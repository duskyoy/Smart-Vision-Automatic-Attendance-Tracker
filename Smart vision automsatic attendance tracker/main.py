import subprocess

if __name__ == "__main__":
    # Run login.py first
    login_process = subprocess.run(["python", "gui/login.py"])
    
    # If login was successful (exit code 0), run dashboard.py
    #if login_process.returncode == 0:
        #subprocess.run(["python", "gui/dashboard.py"])
else:
    print("Login failed. Exiting the system.")
