"""
AICTE Compliance - Comprehensive Update Script
This script updates all remaining files to achieve 100% AICTE compliance
"""

import os
import re
from pathlib import Path

# Define the project root
PROJECT_ROOT = Path(__file__).parent

# Terminology mappings
TERMINOLOGY_MAP = {
    # Backend
    'Job': 'Internship',
    'job': 'internship',
    'jobs': 'internships',
    'Jobs': 'Internships',
    'Candidate': 'Student',
    'candidate': 'student',
    'candidates': 'students',
    'Candidates': 'Students',
    'company': 'organization',
    'Company': 'Organization',
    'companies': 'organizations',
    'Companies': 'Organizations',
    'job_type': 'internship_type',
    'job_id': 'internship_id',
    'candidate_id': 'student_id',
    
    # Keep these specific patterns
    'job_title': 'internship_title',
    'job.title': 'internship.title',
    'job.company': 'internship.organization',
}

def update_file_content(file_path, replacements):
    """Update file content with terminology replacements"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Only write if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def update_backend_files():
    """Update all backend Python files"""
    backend_root = PROJECT_ROOT / 'backend'
    
    files_to_update = [
        'app/api/endpoints/ai_routes.py',
        'app/api/endpoints/insights.py',
        'app/api/endpoints/auth.py',
        'app/services/resume_parser.py',
        'app/services/job_analyzer.py',
        'app/services/matcher.py',
        'add_test_job.py',
        'test_auth.py',
        'inspect_db.py',
    ]
    
    updated_count = 0
    for file_path in files_to_update:
        full_path = backend_root / file_path
        if full_path.exists():
            if update_file_content(full_path, TERMINOLOGY_MAP):
                updated_count += 1
                print(f"✓ Updated: {file_path}")
    
    print(f"\n✅ Backend: {updated_count} files updated")

def update_frontend_files():
    """Update all frontend TypeScript/TSX files"""
    frontend_root = PROJECT_ROOT / 'frontend'
    
    # Get all .tsx and .ts files
    tsx_files = list(frontend_root.rglob('*.tsx'))
    ts_files = list(frontend_root.rglob('*.ts'))
    
    all_files = tsx_files + ts_files
    
    # Exclude node_modules and .next
    all_files = [f for f in all_files if 'node_modules' not in str(f) and '.next' not in str(f)]
    
    updated_count = 0
    for file_path in all_files:
        if update_file_content(file_path, TERMINOLOGY_MAP):
            updated_count += 1
            print(f"✓ Updated: {file_path.relative_to(frontend_root)}")
    
    print(f"\n✅ Frontend: {updated_count} files updated")

def main():
    print("=" * 60)
    print("AICTE COMPLIANCE - COMPREHENSIVE UPDATE")
    print("=" * 60)
    print()
    
    print("Phase 1: Updating Backend Files...")
    print("-" * 60)
    update_backend_files()
    
    print()
    print("Phase 2: Updating Frontend Files...")
    print("-" * 60)
    update_frontend_files()
    
    print()
    print("=" * 60)
    print("✅ AICTE COMPLIANCE UPDATE COMPLETE")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("1. Restart backend server: python -m uvicorn main:app --reload --port 8003")
    print("2. Frontend will auto-reload")
    print("3. Test all functionality")

if __name__ == "__main__":
    main()
