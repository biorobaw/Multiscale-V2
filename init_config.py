import os

if not os.path.exists("../scs"):
    print("[+] cloning scs...")
    os.system("git clone https://github.com/biorobaw/scs.git ../scs")
else:
    print("[+] skip cloning scs")


print("[+] setting up git to prevent modifying configuration files...")
os.system("git update-index --skip-worktree .idea/runConfigurations/Multiscale_testing.xml")

print("[+] set up complete.")

