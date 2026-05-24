# Plan for Organizing S24+ Phone Storage

The user wants to move "unnecessary or old" files from their S24+ phone to a backup folder on drive E: if the files were created/modified before January 1, 2026.

## Target Details
- **Source**: Kevin의 S24+ -> 내장 저장공간 (Internal Storage)
- **Destination**: `E:\20260502 S24 백업`
- **Threshold Date**: 2026-01-01

## Challenges
- **MTP Access**: The phone is an MTP device, so it doesn't have a drive letter. We must use `Shell.Application` COM objects.
- **Performance**: Moving files over MTP can be slow, especially with 223GB of data.
- **Recursive Scan**: We need to traverse all folders in the storage.

## Proposed Strategy
1. **Identify Storage**: Locate the "내장 저장공간" folder on the phone.
2. **Recursive Traversal**:
   - For each file found, check the `ModifyDate`.
   - If `ModifyDate < 2026-01-01`, proceed to move.
3. **Move Logic**:
   - Create the corresponding directory structure in the destination.
   - Copy the file to the destination.
   - Verify the copy was successful.
   - Delete the file from the source (to effectively "move").
4. **Safety**:
   - Skip system folders like `Android` to avoid moving app data.
   - Focus on media and user data: `DCIM`, `Pictures`, `Download`, `Movies`, `Music`, `Documents`.

## Proposed Script
A PowerShell script will be used to automate this.

### [NEW] organize_phone.ps1
This script will perform the move operation.

## Verification Plan
1. **Dry Run**: First, list the files that *would* be moved without actually moving them.
2. **Incremental Execution**: Move a small batch first to ensure stability.
3. **Final Move**: Perform the full operation.
