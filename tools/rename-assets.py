from pathlib import Path
import runpy
# Collect image names without running the generator by parsing its dictionary.
import ast
source=Path(__file__).with_name('build.py').read_text()
module=ast.parse(source)
media=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MEDIA' for t in n.targets))
root=Path(__file__).resolve().parents[1]/'assets'/'img'
for i,slug in media.items():
 old=root/f'{i:02d}.webp';new=root/f'{i:02d}-{slug}.webp'
 if old.exists():old.rename(new)
assert len(list(root.glob('*.webp')))==28
print('Named 28 images')
