#!/usr/bin/env node

const { execSync, spawn } = require("child_process");
const path = require("path");
const fs = require("fs");
const os = require("os");

const REPO_URL = "https://github.com/Runa798/fathomx.git";
const CLONE_DIR = path.join(os.tmpdir(), "fathomx-install");

function run(cmd, opts = {}) {
  return execSync(cmd, { stdio: "inherit", ...opts });
}

function runSetup() {
  const child = spawn("python3", ["-m", "fathomx", "setup"], {
    stdio: "inherit",
    env: { ...process.env },
  });

  child.on("close", (code) => {
    process.exit(code);
  });
}

function main() {
  if (os.platform() === "win32") {
    console.error("\nWindows is not directly supported. Please use WSL2:");
    console.error("  wsl npx fathomx\n");
    process.exit(1);
  }

  const args = process.argv.slice(2);
  const isUninstall = args.includes("--uninstall");
  const invokedAs = path.basename(process.argv[1] || "");
  const isSetup = args.includes("--setup") || invokedAs === "fathomx-setup";

  console.log("\n🔍 FathomX — Installer\n");

  if (isSetup) {
    runSetup();
    return;
  }

  if (isUninstall) {
    console.log("Running uninstall...\n");
    const skillTarget = path.join(os.homedir(), ".claude", "skills", "fathomx");
    try {
      run("claude mcp remove grok-search 2>/dev/null || true");
      run("claude mcp remove exa 2>/dev/null || true");
      if (fs.existsSync(skillTarget)) {
        fs.rmSync(skillTarget, { recursive: true, force: true });
        console.log(`Removed: ${skillTarget}`);
      }
      console.log("\n✅ Uninstall complete.\n");
    } catch (e) {
      console.error("Uninstall error:", e.message);
      process.exit(1);
    }
    return;
  }

  if (fs.existsSync(CLONE_DIR)) {
    fs.rmSync(CLONE_DIR, { recursive: true, force: true });
  }

  console.log("Cloning repository...");
  run(`git clone --depth 1 ${REPO_URL} "${CLONE_DIR}"`);

  const envExample = path.join(CLONE_DIR, ".env.example");
  const envTarget = path.join(CLONE_DIR, ".env");
  if (!fs.existsSync(envTarget) && fs.existsSync(envExample)) {
    fs.copyFileSync(envExample, envTarget);
    console.log("\nCreated .env from .env.example");
    console.log("⚠️  Edit API keys before running install.sh:");
    console.log(`   ${envTarget}\n`);
  }

  console.log("Running install.sh...\n");
  const installScript = path.join(CLONE_DIR, "install.sh");
  fs.chmodSync(installScript, "755");

  const child = spawn("bash", [installScript], {
    cwd: CLONE_DIR,
    stdio: "inherit",
    env: { ...process.env },
  });

  child.on("close", (code) => {
    if (code === 0) {
      console.log("\n💡 To launch the full setup TUI:");
      console.log("   npx fathomx --setup");
      console.log("   or: python3 -m fathomx setup");
      console.log("\n💡 To configure API keys later:");
      console.log(`   cd ${CLONE_DIR} && $EDITOR .env && ./install.sh\n`);
    }
    process.exit(code);
  });
}

main();
