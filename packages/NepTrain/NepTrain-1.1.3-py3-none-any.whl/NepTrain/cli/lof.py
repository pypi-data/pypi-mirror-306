import pyfiglet
from rich.console import Console
from rich.text import Text

# 使用 pyfiglet 生成 ASCII 字体
text = "NepTrain"
ascii_logo = pyfiglet.figlet_format(text, font="slant")

# 使用 rich 打印彩色 Logo
console = Console()
rich_text = Text(ascii_logo, style="bold magenta")  # 设置字体样式和颜色
console.print(rich_text)
fonts = pyfiglet.FigletFont.getFonts()
print(fonts)