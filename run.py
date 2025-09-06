#!/usr/bin/env python3
"""
Cross-platform test runner for FindWord
Modern Python script replacing traditional shell scripts
"""

import subprocess
import sys
import os
import platform
import json
from pathlib import Path
from typing import List, Dict, Any

class Colors:
    """ANSI color codes for cross-platform terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    NC = '\033[0m'  # No Color

class CrossPlatformRunner:
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.python_cmd = self._get_python_command()
        self.cmake_cmd = self._get_cmake_command()
        
    def _get_python_command(self) -> str:
        """Get the appropriate Python command for the platform"""
        commands = ["python3", "python"]
        for cmd in commands:
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd
            except FileNotFoundError:
                continue
        raise RuntimeError("Python not found in PATH")
    
    def _get_cmake_command(self) -> str:
        """Get the appropriate CMake command"""
        try:
            result = subprocess.run(["cmake", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return "cmake"
        except FileNotFoundError:
            pass
        raise RuntimeError("CMake not found in PATH")
    
    def run_command(self, command: List[str], cwd: str = None, 
                   capture_output: bool = False) -> subprocess.CompletedProcess:
        """Run a command with proper error handling"""
        try:
            print(f"{Colors.CYAN}Running: {' '.join(command)}{Colors.NC}")
            result = subprocess.run(command, cwd=cwd, capture_output=capture_output, 
                                  text=True, check=False)
            
            if result.returncode != 0:
                print(f"{Colors.RED}Command failed with exit code {result.returncode}{Colors.NC}")
                if capture_output:
                    print(f"stdout: {result.stdout}")
                    print(f"stderr: {result.stderr}")
            
            return result
        except FileNotFoundError as e:
            print(f"{Colors.RED}Command not found: {e}{Colors.NC}")
            raise
    
    def setup_environment(self):
        """Set up the development environment"""
        print(f"{Colors.YELLOW}Setting up development environment...{Colors.NC}")
        
        # Create virtual environment
        venv_dir = "venv"
        if self.is_windows:
            venv_python = f"{venv_dir}\\Scripts\\python.exe"
            venv_pip = f"{venv_dir}\\Scripts\\pip.exe"
        else:
            venv_python = f"{venv_dir}/bin/python"
            venv_pip = f"{venv_dir}/bin/pip"
        
        # Create venv if it doesn't exist
        if not os.path.exists(venv_dir):
            self.run_command([self.python_cmd, "-m", "venv", venv_dir])
        
        # Install requirements
        if os.path.exists("requirements.txt.in"):
            self.run_command([venv_python, "-m", "pip", "install", "-r", "requirements.txt.in"])
        
        print(f"{Colors.GREEN}Environment setup complete{Colors.NC}")
    
    def build_project(self, build_type: str = "Release"):
        """Build the project using CMake"""
        print(f"{Colors.YELLOW}Building project ({build_type})...{Colors.NC}")
        
        # Use CMake presets if available
        if os.path.exists("CMakePresets.json"):
            preset_name = "default" if build_type == "Release" else "debug"
            
            # Configure
            result = self.run_command([self.cmake_cmd, "--preset", preset_name])
            if result.returncode != 0:
                # Fallback to manual configuration
                build_dir = f"build/{preset_name}"
                os.makedirs(build_dir, exist_ok=True)
                self.run_command([self.cmake_cmd, "-B", build_dir, 
                                f"-DCMAKE_BUILD_TYPE={build_type}"])
            
            # Build
            self.run_command([self.cmake_cmd, "--build", f"build/{preset_name}"])
        else:
            # Fallback to traditional CMake
            build_dir = "build"
            os.makedirs(build_dir, exist_ok=True)
            self.run_command([self.cmake_cmd, "-B", build_dir, 
                            f"-DCMAKE_BUILD_TYPE={build_type}"])
            self.run_command([self.cmake_cmd, "--build", build_dir])
        
        print(f"{Colors.GREEN}Build complete{Colors.NC}")
    
    def run_tests(self):
        """Run all tests"""
        print(f"{Colors.YELLOW}Running tests...{Colors.NC}")
        
        # Run CMake tests if available
        test_dirs = ["build/default", "build/release", "build"]
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                result = self.run_command(["ctest", "--output-on-failure"], cwd=test_dir)
                if result.returncode == 0:
                    break
        
        # Run Python integration tests
        test_script = Path("tests/test_integration.py")
        if test_script.exists():
            self.run_command([self.python_cmd, str(test_script)])
        
        print(f"{Colors.GREEN}Tests complete{Colors.NC}")
    
    def package_project(self):
        """Package the project for distribution"""
        print(f"{Colors.YELLOW}Packaging project...{Colors.NC}")
        
        build_dirs = ["build/default", "build/release", "build"]
        for build_dir in build_dirs:
            if os.path.exists(build_dir):
                self.run_command([self.cmake_cmd, "--build", build_dir, "--target", "package"])
                break
        
        print(f"{Colors.GREEN}Packaging complete{Colors.NC}")
    
    def clean_project(self):
        """Clean build artifacts"""
        print(f"{Colors.YELLOW}Cleaning project...{Colors.NC}")
        
        # Remove build directories
        import shutil
        dirs_to_remove = ["build", "venv"]
        for dir_name in dirs_to_remove:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"Removed {dir_name}/")
        
        # Remove temporary files
        files_to_remove = ["permutated_words.txt", "*.exe", "findword"]
        for pattern in files_to_remove:
            import glob
            for file in glob.glob(pattern):
                if os.path.exists(file):
                    os.remove(file)
                    print(f"Removed {file}")
        
        print(f"{Colors.GREEN}Cleaning complete{Colors.NC}")
    
    def show_info(self):
        """Show system and project information"""
        print(f"{Colors.BLUE}System Information{Colors.NC}")
        print(f"Platform: {platform.platform()}")
        print(f"Python: {self.python_cmd} ({platform.python_version()})")
        print(f"CMake: {self.cmake_cmd}")
        
        # Check for C++ compiler
        compilers = ["g++", "clang++", "cl"]
        for compiler in compilers:
            try:
                result = subprocess.run([compiler, "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"C++ Compiler: {compiler}")
                    break
            except FileNotFoundError:
                continue

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cross-platform build and test runner")
    parser.add_argument("command", choices=[
        "setup", "build", "test", "package", "clean", "info", "all"
    ], help="Command to run")
    parser.add_argument("--debug", action="store_true", help="Use debug build")
    
    args = parser.parse_args()
    
    runner = CrossPlatformRunner()
    
    try:
        if args.command == "setup":
            runner.setup_environment()
        elif args.command == "build":
            build_type = "Debug" if args.debug else "Release"
            runner.build_project(build_type)
        elif args.command == "test":
            runner.run_tests()
        elif args.command == "package":
            runner.package_project()
        elif args.command == "clean":
            runner.clean_project()
        elif args.command == "info":
            runner.show_info()
        elif args.command == "all":
            runner.setup_environment()
            build_type = "Debug" if args.debug else "Release"
            runner.build_project(build_type)
            runner.run_tests()
        
        print(f"{Colors.GREEN}Command '{args.command}' completed successfully{Colors.NC}")
        
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.NC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
