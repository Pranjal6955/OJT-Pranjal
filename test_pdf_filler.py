#!/usr/bin/env python3
"""
Test script to verify PDF filler functionality.
Fills ojt_template.pdf with test data for all fields and saves output as abc_filled.pdf
"""

import os
from pdf_filler import fill_pdf_with_overlay

def test_pdf_filler():
    """Test filling PDF with sample data for all fields."""
    
    # Check if ojt_template.pdf exists
    pdf_path = "ojt_template.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ Error: {pdf_path} not found in current directory")
        return False
    
    print(f"✓ Found {pdf_path}")
    
    # Read the PDF template
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    print(f"✓ Loaded PDF ({len(pdf_bytes)} bytes)")
    
    # Create test data for all fields
    test_data = [
        # Page 1: Standard data with bullet points (new feature)
        {
            "date": "23-3-2026",
            "ojt_timing": "3:30 PM – 6:30 PM",
            "department": "Engineering",
            "designation": "Software Intern",
            "my_space": "One short sentence for reflection.",
            "tasks_carried_out": "• Task 1: Implemented UI\n• Task 2: Fixed bugs\n• Task 3: Wrote tests",
            "key_learnings": "• Learned React hooks\n• Improved Git workflow\n• Understood PDF generation",
            "tools_used": "Python, React, Git, VS Code",
            "special_achievements": "Completed all tasks today.",
        },
        # Page 2: Long text to test truncation (max_lines)
        {
            "date": "24-3-2026",
            "ojt_timing": "9:00 AM – 5:00 PM",
            "department": "Engineering",
            "designation": "Software Intern",
            "my_space": "This is a very long reflection that might exceed the four lines limit if it was even longer than this, but we want to see how it handles standard text wrapping at the new font size of 11.",
            "tasks_carried_out": "• Line 1\n• Line 2\n• Line 3\n• Line 4\n• Line 5\n• Line 6\n• Line 7 (this should be truncated as max_lines is 6)",
            "key_learnings": "• Learning 1\n• Learning 2\n• Learning 3\n• Learning 4\n• Learning 5 (this should be truncated as max_lines is 4)",
            "tools_used": "Very Long Tool Name 1, Very Long Tool Name 2, Very Long Tool Name 3, Very Long Tool Name 4 (testing width)",
            "special_achievements": "This is a very long achievement description to test if it wraps correctly within its 240 width boundary at font size 11.",
        }
    ]
    
    print("\n📝 Test data fields:")
    for key, value in test_data[0].items():
        preview = value[:50] + "..." if len(value) > 50 else value
        print(f"  • {key}: {preview}")
    
    # Fill the PDF
    try:
        filled_pdf = fill_pdf_with_overlay(pdf_bytes, test_data)
        print(f"\n✓ PDF filled successfully ({len(filled_pdf)} bytes)")
    except Exception as e:
        print(f"\n❌ Error filling PDF: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Save the filled PDF
    output_path = "abc_filled.pdf"
    with open(output_path, "wb") as f:
        f.write(filled_pdf)
    print(f"✓ Saved filled PDF to {output_path}")
    
    print("\n✅ Test completed successfully!")
    print(f"\nNext steps:")
    print(f"1. Open {output_path} to verify fields are filled correctly")
    print(f"2. Check that all text is visible and properly positioned")
    print(f"3. Verify text wrapping for multi-line fields (my_space, tasks_carried_out, etc.)")
    
    return True

if __name__ == "__main__":
    test_pdf_filler()
