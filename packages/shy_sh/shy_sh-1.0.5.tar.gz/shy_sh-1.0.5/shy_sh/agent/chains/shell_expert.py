import os
import re
from tempfile import NamedTemporaryFile
import subprocess
import pyperclip
from time import strftime
from rich.syntax import Syntax
from shy_sh.agent.models import FinalResponse
from langchain_core.runnables import chain
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from shy_sh.agent.chat_models import get_llm
from shy_sh.agent.utils import ask_confirm, decode_output, detect_shell, detect_os
from textwrap import dedent
from rich import print
from rich.live import Live


sys_template = dedent(
    """
    Output only a block of code like this:
    ```sh
    #!/bin/sh
    set -e
    [your shell script]
    ```

    This is a template for sh, but you should use the right shell syntaxt depending on your system.
    Don't write interactive commands or install new packages if not explicitly requested.
    Write a shell script that accomplishes the task.

    Task: {input}
    """
)


@chain
def _chain(_):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a shell expert. The current date and time is {timestamp}\nYou are running on {system} using {shell} as shell",
            ),
            MessagesPlaceholder("history", optional=True),
            ("human", sys_template),
        ]
    )
    return prompt | llm | StrOutputParser()


def shell_expert_chain(task: str, history, ask_before_execute: bool):
    print(f"💻 [bold dark_green]Generating shell script...[/bold dark_green]\n")
    shell = detect_shell()
    system = detect_os()
    inputs = {
        "input": task,
        "timestamp": strftime("%Y-%m-%d %H:%M %Z"),
        "history": history,
        "system": system,
        "shell": shell,
    }
    code = ""
    with Live() as live:
        for chunk in _chain.stream(inputs):
            code += chunk
            live.update(
                Syntax(code, "console", background_color="#212121"), refresh=True
            )

        code = re.sub(r"```\S+\n", "", code).replace("```", "")
        live.update(
            Syntax(code.strip(), "console", background_color="#212121"), refresh=True
        )

    confirm = "y"
    if ask_before_execute:
        confirm = ask_confirm()
    print()
    if confirm == "n":
        return FinalResponse(response="Task interrupted")
    elif confirm == "c":
        pyperclip.copy(code)
        return FinalResponse(response="Script copied to the clipboard!")

    ext = ".sh"
    if shell == "cmd":
        ext = ".bat"
    elif shell == "powershell":
        ext = ".ps1"
    with NamedTemporaryFile("w+", suffix=ext, delete_on_close=False) as file:
        file.write(code)
        file.close()
        os.chmod(file.name, 0o755)
        result = subprocess.run(
            file.name,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        stdout = decode_output(result) or "Done"
    print()
    print(Syntax(stdout.strip(), "console", background_color="#212121"))
    return f"Script executed:\n{code}\n\nOutput:\n{stdout}"
