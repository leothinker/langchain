code = compile("def hi(x): return f'Hi, {x}!'", "<string>", "exec")
ns = {}
exec(code, ns)
hi = ns["hi"]
print(hi("World"))  # 输出 Hi, World!
