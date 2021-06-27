import os

if not os.path.exists("../scs"):
    print("[+] cloning scs...")
    os.system("git clone git@github.com:biorobaw/scs.git ../")
else:
    print("[+] skip cloning scs")


print("[+] setting up git to prevent modifying configuration files...")
os.system("git update-index --skip-worktree .idea/runConfigurations/Multiscale_testing.xml")

print("[+] set up complete.")

