from pathlib import Path
from typing import Final

import typer
from beni import bcolor, bpath, btask
from beni.bfunc import syncCall

from ..common.func import useResources
from .venv import venv

app: Final = btask.app


@app.command('project')
@syncCall
async def _(
    workspace_path: Path = typer.Option(None, '--path', help='workspace 路径'),
):
    '生成新项目'

    workspace_path = workspace_path or Path.cwd()

    # 检查目标路径是否合法
    if not workspace_path.exists():
        pass  # 不存在，允许继续创建
    elif not workspace_path.is_dir():
        bcolor.printRed('目标路径不是一个目录', workspace_path)
        return
    elif list(bpath.get(workspace_path).glob('*')):
        bcolor.printRed('目标路径不是空目录', workspace_path)
        return

    venv(['benimang'], workspace_path, False, False, False, False)
    with useResources('project') as sourceProjectPath:
        bpath.copyOverwrite(sourceProjectPath, workspace_path)
