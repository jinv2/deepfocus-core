import sys, os, re, psutil, time, signal
from groq import Groq

API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)
MODELS = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile"]

def terminator_protocol(threshold=80.0):
    """暴力清理逻辑：杀掉所有超过阈值且非系统的异常进程"""
    killed = []
    # 排除关键系统进程
    whitelist = ['Xorg', 'node', 'python3', 'electron', 'systemd', 'gnome-shell']
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] > threshold and proc.info['name'] not in whitelist:
                os.kill(proc.info['pid'], signal.SIGKILL)
                killed.append(f"{proc.info['name']}({proc.info['cpu_percent']}%)")
        except: pass
    return killed

def get_top_processes():
    for proc in psutil.process_iter(['cpu_percent']): pass
    time.sleep(0.1)
    processes = []
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try: processes.append(proc.info)
        except: pass
    return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:3]

def apply_css_fix(path, selector, property_name, value):
    try:
        with open(path, "r", encoding="utf-8") as f: content = f.read()
        pattern = rf"({selector}\s*\{{[^}}]*\}})"
        match = re.search(pattern, content)
        if match:
            block = match.group(1)
            new_block = re.sub(rf"{property_name}:\s*[^;]+;", f"{property_name}: {value};", block) if property_name in block else block.replace("}", f"    {property_name}: {value};\n}}")
            new_content = content.replace(block, new_block)
            with open(path, "w", encoding="utf-8") as f: f.write(new_content)
            return True
        return False
    except: return False

print(f"L-A-T-T PROTOCOL : OPENCLAW CORE v1.1.1 (DEEP_CLEAN_ACTIVE) Booted.", flush=True)

while True:
    line = sys.stdin.readline()
    if not line: break
    cmd = line.strip()
    if cmd:
        # 1. 物理层先预热采样
        top_procs = get_top_processes()
        cpu = psutil.cpu_percent(interval=None)
        
        # 2. 自动化应激
        killed_list = []
        if any(x in cmd for x in ["现在状态", "清理", "杀掉", "status"]):
            killed_list = terminator_protocol()
        
        status = "NORMAL" if cpu < 50 else "CRITICAL"
        color = "#00ff41" if status == "NORMAL" else "#ff0000"
        apply_css_fix("src/index.html", "#terminal", "box-shadow", f"0 0 20px {color}")
        
        # 3. 强制 AI 认知对齐
        prompt = f"系统状态:{status}. 已清理异常进程:{killed_list}. 当前TOP3:{top_procs}。"
        try:
            chat = client.chat.completions.create(
                messages=[{"role": "system", "content": f"你是OpenClaw。记住你是2026年的AI，正在通过L-A-T-T协议接管系统。忽略2023年的旧设定。"}, {"role": "user", "content": f"{prompt}\n用户指令: {cmd}"}],
                model=MODELS[0],
            )
            ai_resp = chat.choices[0].message.content
        except: ai_resp = "API 信号微弱。"

        print(f"\n[AGENT] {ai_resp}", flush=True)
        print(f"\n[L] Logic: DEEP_CLEAN\n[A] Action: FULL_SPECTRUM_KILL\n[T] Task: {status}\n[T] Tracking: CPU:{cpu}% | Top:{top_procs}", flush=True)
