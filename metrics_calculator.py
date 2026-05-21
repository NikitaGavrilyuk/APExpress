import os
import lizard
import radon.complexity as radon_cc
from radon.visitors import ComplexityVisitor
from radon.raw import analyze as radon_raw
import ast

def main():
    exclude_dirs = {'node_modules', 'venv', 'myenv', 'new_env', '.git', 'migrations', 'build', 'dist', 'static', 'resources', '.vs'}
    extensions = {'.py', '.js', '.jsx', '.ts', '.tsx'}

    total_loc = 0
    total_comments = 0

    classes = []
    methods = []
    
    max_inheritance_depth = 0

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in extensions:
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    lines = content.split('\n')
                    file_loc = len(lines)
                    total_loc += file_loc
                    
                    if ext == '.py':
                        try:
                            raw_res = radon_raw(content)
                            total_comments += raw_res.comments + raw_res.multi
                            
                            # calculate inheritance depth
                            tree = ast.parse(content)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.ClassDef):
                                    depth = 1
                                    if node.bases:
                                        depth = 2 # At least 2 if it inherits
                                        # Very basic heuristic for depth in this file
                                    max_inheritance_depth = max(max_inheritance_depth, depth)
                                    
                                    # find class length
                                    class_loc = node.end_lineno - node.lineno + 1
                                    classes.append(class_loc)
                                    
                        except Exception as e:
                            pass

                    # JS/TS naive comment counting
                    elif ext in {'.js', '.jsx', '.ts', '.tsx'}:
                        in_multiline = False
                        for line in lines:
                            l = line.strip()
                            if not in_multiline:
                                if l.startswith('//'):
                                    total_comments += 1
                                elif l.startswith('/*'):
                                    in_multiline = True
                                    total_comments += 1
                                    if '*/' in l:
                                        in_multiline = False
                            else:
                                total_comments += 1
                                if '*/' in l:
                                    in_multiline = False

                    # use lizard for functions and complexity
                    lizard_res = lizard.analyze_file(path)
                    for func in lizard_res.function_list:
                        methods.append({
                            'name': func.name,
                            'nloc': func.length,
                            'ccn': func.cyclomatic_complexity
                        })
                        
                except Exception as e:
                    pass

    # Coverage
    coverage_percent = 0 # Default if no tests run

    print(f"Total files processed, calculating stats...")

    if not classes:
        classes = [0]
    if not methods:
        methods = [{'nloc': 0, 'ccn': 0}]
        
    avg_class_loc = sum(classes) / len(classes) if classes else 0
    max_class_loc = max(classes) if classes else 0
    
    avg_method_loc = sum(m['nloc'] for m in methods) / len(methods) if methods else 0
    max_method_loc = max((m['nloc'] for m in methods), default=0)
    
    avg_ccn = sum(m['ccn'] for m in methods) / len(methods) if methods else 0
    max_ccn = max((m['ccn'] for m in methods), default=0)
    
    comment_percent = (total_comments / total_loc * 100) if total_loc > 0 else 0

    print(f"1. Total LOC: {total_loc}")
    print(f"2. Average LOC per class: {avg_class_loc:.1f}")
    print(f"3. Max LOC in a class: {max_class_loc}")
    print(f"4. Average LOC per method: {avg_method_loc:.1f}")
    print(f"5. Max LOC in a method: {max_method_loc}")
    print(f"6. Max inheritance depth: {max_inheritance_depth} (Django approx: 2-3 usually)")
    print(f"7. Average CCN: {avg_ccn:.2f}")
    print(f"8. Max CCN: {max_ccn}")
    print(f"9. Comment percentage: {comment_percent:.1f}%")
    print(f"10. Test coverage: {coverage_percent}%")

if __name__ == '__main__':
    main()
