const { exec } = require('child_process');
const path = require('path');

// 自动定位内核路径
const scriptPath = path.join(__dirname, 'core_v1_1.py');
const testQuery = "自动生成的MVP指令";

console.log("🔗 正在尝试连接 L-A-T-T 内核...");

exec(`python3 "${scriptPath}" "${testQuery}"`, (error, stdout, stderr) => {
    if (error) {
        console.error("❌ 桥接通讯故障:", stderr);
        return;
    }
    try {
        const response = JSON.parse(stdout);
        console.log("✅ 桥接成功！内核版本:", response.version);
        console.log("📋 拆解逻辑已同步:", response.data.mvp_steps[0]);
    } catch (e) {
        console.error("❌ 格式化错误: 内核返回了非 JSON 杂质", stdout);
    }
});
