#!/usr/bin/env python3
"""
Master test runner for Vicsek model project.
Provides an interactive menu for running tests in various modes.
"""

import subprocess
import sys
import os
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")


def run_command(cmd, description):
    """Run a shell command and return success status."""
    print_info(f"Running: {description}")
    print(f"{Colors.YELLOW}Command: {' '.join(cmd)}{Colors.END}\n")
    
    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            print_success(f"{description} completed successfully!")
            return True
        else:
            print_error(f"{description} failed with return code {result.returncode}")
            return False
    except FileNotFoundError:
        print_error(f"Command not found: {cmd[0]}")
        print_info("Make sure pytest is installed: pip install pytest pytest-cov")
        return False
    except KeyboardInterrupt:
        print_error("\nTest run interrupted by user")
        return False


def check_pytest_installed():
    """Check if pytest is installed."""
    try:
        result = subprocess.run(['pytest', '--version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print_success(f"pytest is installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print_error("pytest is not installed!")
    print_info("Install with: pip install pytest pytest-cov")
    return False


def check_project_structure():
    """Check if project structure is correct."""
    required_files = [
        'config.py',
        'state.py',
        'dynamics.py',
        'neighborhood.py',
        'diagnostics.py',
        'tests/__init__.py',
        'tests/test_initialization.py',
        'tests/test_neighborhood.py',
        'tests/test_dynamics.py',
        'tests/test_diagnostics.py',
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print_error("Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print_success("Project structure is correct")
    return True


def run_all_tests():
    """Run all tests with verbose output."""
    print_header("Running All Tests")
    return run_command(['pytest', '-v'], "All tests")


def run_all_tests_with_coverage():
    """Run all tests with coverage report."""
    print_header("Running All Tests with Coverage")
    success = run_command(
        ['pytest', '-v', '--cov=.', '--cov-report=term-missing', '--cov-report=html'],
        "Tests with coverage"
    )
    if success:
        print_info("\nHTML coverage report generated in: htmlcov/index.html")
    return success


def run_quick_tests():
    """Run tests with early exit on first failure."""
    print_header("Quick Test Run (stops at first failure)")
    return run_command(['pytest', '-v', '-x'], "Quick tests")


def run_specific_module():
    """Run tests for a specific module."""
    print_header("Run Specific Test Module")
    
    modules = {
        '1': ('tests/test_initialization.py', 'Initialization tests'),
        '2': ('tests/test_neighborhood.py', 'Neighborhood tests'),
        '3': ('tests/test_dynamics.py', 'Dynamics tests'),
        '4': ('tests/test_diagnostics.py', 'Diagnostics tests'),
    }
    
    print("Available test modules:")
    for key, (path, desc) in modules.items():
        print(f"  {key}. {desc}")
    print("  0. Back to main menu")
    
    choice = input("\nSelect module (0-4): ").strip()
    
    if choice == '0':
        return True
    elif choice in modules:
        path, desc = modules[choice]
        print()
        return run_command(['pytest', '-v', path], desc)
    else:
        print_error("Invalid choice")
        return False


def run_tests_by_keyword():
    """Run tests matching a keyword."""
    print_header("Run Tests by Keyword")
    
    print("Common keywords:")
    print("  - order (order parameter tests)")
    print("  - periodic (periodic boundary tests)")
    print("  - neighbor (neighborhood tests)")
    print("  - wrap (boundary wrapping tests)")
    print("  - heading (heading-related tests)")
    
    keyword = input("\nEnter keyword (or 'back' to return): ").strip()
    
    if keyword.lower() == 'back':
        return True
    
    if keyword:
        return run_command(['pytest', '-v', '-k', keyword], 
                         f"Tests matching '{keyword}'")
    else:
        print_error("No keyword provided")
        return False


def run_failed_tests():
    """Re-run only failed tests from last run."""
    print_header("Re-run Failed Tests")
    return run_command(['pytest', '-v', '--lf'], "Failed tests only")


def run_with_debug():
    """Run tests with debug output (show print statements)."""
    print_header("Run Tests with Debug Output")
    return run_command(['pytest', '-v', '-s', '-l'], "Tests with debug output")


def run_parallel_tests():
    """Run tests in parallel."""
    print_header("Run Tests in Parallel")
    
    # Check if pytest-xdist is installed
    try:
        subprocess.run(['pytest', '--version'], 
                      capture_output=True, 
                      check=True)
        result = subprocess.run(['pip', 'show', 'pytest-xdist'],
                              capture_output=True,
                              text=True)
        
        if result.returncode != 0:
            print_error("pytest-xdist is not installed")
            install = input("Install pytest-xdist? (y/n): ").strip().lower()
            if install == 'y':
                subprocess.run(['pip', 'install', 'pytest-xdist'])
            else:
                return False
        
        return run_command(['pytest', '-v', '-n', 'auto'], 
                         "Parallel tests (using all CPU cores)")
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def collect_tests():
    """Show all discoverable tests without running them."""
    print_header("Collect Tests (Discovery)")
    return run_command(['pytest', '--collect-only'], "Test discovery")


def clean_cache():
    """Clean pytest cache and coverage files."""
    print_header("Clean Cache and Coverage Files")
    
    items_to_remove = [
        '.pytest_cache',
        '__pycache__',
        'tests/__pycache__',
        '.coverage',
        'htmlcov',
        '*.pyc',
    ]
    
    print("Cleaning:")
    for item in items_to_remove:
        print(f"  - {item}")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print_info("Cancelled")
        return True
    
    # Remove directories and files
    import shutil
    
    for item in ['.pytest_cache', '__pycache__', 'tests/__pycache__', 
                 '.coverage', 'htmlcov']:
        if Path(item).exists():
            if Path(item).is_dir():
                shutil.rmtree(item)
                print_success(f"Removed {item}/")
            else:
                Path(item).unlink()
                print_success(f"Removed {item}")
    
    # Remove .pyc files
    for pyc in Path('.').rglob('*.pyc'):
        pyc.unlink()
        print_success(f"Removed {pyc}")
    
    print_success("\nCleanup complete!")
    return True


def run_comprehensive_check():
    """Run comprehensive pre-commit check."""
    print_header("Comprehensive Pre-Commit Check")
    
    checks = [
        (check_project_structure, "Project structure check"),
        (lambda: run_command(['pytest', '-v'], "All tests"),
         "Running all tests"),
        (lambda: run_command(['pytest', '--cov=.', '--cov-report=term-missing'],
                           "Coverage check"),
         "Coverage analysis"),
    ]
    
    all_passed = True
    for i, (check_func, description) in enumerate(checks, 1):
        print(f"\n{Colors.BOLD}Check {i}/{len(checks)}: {description}{Colors.END}")
        if not check_func():
            all_passed = False
            print_error(f"Check failed: {description}")
            break
        print_success(f"Check passed: {description}")
    
    print()
    if all_passed:
        print_success("All checks passed! ✓")
        print_info("Your code is ready to commit!")
    else:
        print_error("Some checks failed! ✗")
        print_info("Please fix the issues before committing.")
    
    return all_passed


def show_coverage_report():
    """Generate and show HTML coverage report."""
    print_header("Generate Coverage Report")
    
    success = run_command(
        ['pytest', '--cov=.', '--cov-report=html'],
        "Generate HTML coverage report"
    )
    
    if success:
        html_file = Path('htmlcov/index.html')
        if html_file.exists():
            print_success(f"\nCoverage report generated: {html_file}")
            
            open_browser = input("Open in browser? (y/n): ").strip().lower()
            if open_browser == 'y':
                import webbrowser
                webbrowser.open(f'file://{html_file.absolute()}')
                print_success("Opened in browser")
    
    return success


def install_dependencies():
    """Install required testing dependencies."""
    print_header("Install Testing Dependencies")
    
    packages = [
        'pytest',
        'pytest-cov',
        'pytest-xdist',  # for parallel testing
    ]
    
    print("Will install:")
    for pkg in packages:
        print(f"  - {pkg}")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print_info("Cancelled")
        return True
    
    for pkg in packages:
        print(f"\nInstalling {pkg}...")
        result = subprocess.run(['pip', 'install', pkg])
        if result.returncode == 0:
            print_success(f"{pkg} installed successfully")
        else:
            print_error(f"Failed to install {pkg}")
    
    return True


def show_menu():
    """Display the main menu."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║         VICSEK MODEL - MASTER TEST RUNNER                      ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚════════════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    print(f"{Colors.BOLD}Quick Tests:{Colors.END}")
    print("  1. Run all tests (verbose)")
    print("  2. Quick test (stop at first failure)")
    print("  3. Re-run failed tests only")
    
    print(f"\n{Colors.BOLD}Coverage & Analysis:{Colors.END}")
    print("  4. Run tests with coverage report")
    print("  5. Generate HTML coverage report")
    
    print(f"\n{Colors.BOLD}Specific Tests:{Colors.END}")
    print("  6. Run specific test module")
    print("  7. Run tests by keyword")
    
    print(f"\n{Colors.BOLD}Advanced:{Colors.END}")
    print("  8. Run tests with debug output")
    print("  9. Run tests in parallel (fast)")
    print(" 10. Collect tests (show all tests)")
    
    print(f"\n{Colors.BOLD}Maintenance:{Colors.END}")
    print(" 11. Clean cache and coverage files")
    print(" 12. Install/update testing dependencies")
    
    print(f"\n{Colors.BOLD}Comprehensive:{Colors.END}")
    print(" 13. Pre-commit check (comprehensive)")
    
    print(f"\n{Colors.BOLD}Other:{Colors.END}")
    print("  0. Exit")
    
    print(f"\n{Colors.YELLOW}{'─'*64}{Colors.END}")

def main():
    """Main program loop."""
    # Check if we're in the right directory
    if not Path('config.py').exists():
        print_error("Error: config.py not found!")
        print_info("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Initial setup check
    print_header("Initial Setup Check")
    if not check_pytest_installed():
        install = input("\nInstall pytest now? (y/n): ").strip().lower()
        if install == 'y':
            subprocess.run(['pip', 'install', 'pytest', 'pytest-cov'])
        else:
            print_error("Cannot proceed without pytest")
            sys.exit(1)
    
    check_project_structure()
    
    # Main menu loop
    while True:
        show_menu()
        choice = input(f"{Colors.BOLD}Enter choice (0-13): {Colors.END}").strip()
        
        actions = {
            '1': run_all_tests,
            '2': run_quick_tests,
            '3': run_failed_tests,
            '4': run_all_tests_with_coverage,
            '5': show_coverage_report,
            '6': run_specific_module,
            '7': run_tests_by_keyword,
            '8': run_with_debug,
            '9': run_parallel_tests,
            '10': collect_tests,
            '11': clean_cache,
            '12': install_dependencies,
            '13': run_comprehensive_check,
            '0': None,  # Exit
        }
        
        if choice == '0':
            print_header("Goodbye!")
            print_success("Thank you for using the Vicsek Model Test Runner!")
            sys.exit(0)
        elif choice in actions:
            try:
                actions[choice]()
            except KeyboardInterrupt:
                print_error("\n\nOperation interrupted by user")
            except Exception as e:
                print_error(f"\n\nUnexpected error: {e}")
                import traceback
                traceback.print_exc()
            
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
        else:
            print_error("Invalid choice! Please enter a number between 0 and 13.")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nProgram interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)