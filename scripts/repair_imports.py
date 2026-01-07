
import os
import re

def fix_imports(directory):
    count = 0
    print(f"Scanning {directory}...")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Regex replacements
                new_content = content
                
                # Replace 'from elysia_core.' with 'from elysia_core.'
                # We need to be careful. 'Core' was the old root.
                # 'Core.Foundation' -> 'elysia_core.Foundation' etc.
                # But wait, looking at the previous grep, key subpackages of Core seem to be directly in elysia_core now?
                # Let's check the structure of elysia_core first.
                
                # Assuming simple mapping for now based on grep results:
                # from elysia_core.X -> from elysia_core.X
                
                new_content = re.sub(r'from Core\.', 'from elysia_core.', new_content)
                new_content = re.sub(r'import Core\.', 'import elysia_core.', new_content)

                if new_content != content:
                    print(f"Fixing {path}")
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
    print(f"Fixed {count} files.")

if __name__ == "__main__":
    # Fix scripts and tests
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fix_imports(os.path.join(base_dir, 'scripts'))
    fix_imports(os.path.join(base_dir, 'tests'))
