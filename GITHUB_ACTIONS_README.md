# GitHub Actions for README Auto-Update

This repository includes GitHub Actions workflows that automatically keep the root `README.md` synchronized with the content from `python-generators-0x00/README.md`.

## Available Workflows

### 1. Basic Workflow (`update-readme.yml`)
- **Trigger**: Push to `python-generators-0x00/README.md` or manual dispatch
- **Action**: Simple copy of content from source to root README
- **Features**: Basic error handling and change detection

### 2. Advanced Workflow (`update-readme-advanced.yml`)
- **Trigger**: Push to `python-generators-0x00/README.md`, manual dispatch, or daily schedule
- **Action**: Copies content with additional header indicating auto-generation
- **Features**: 
  - Enhanced error handling
  - Daily sync schedule (midnight UTC)
  - Better commit messages
  - Proper permissions setup

## How It Works

1. **Trigger**: When you push changes to `python-generators-0x00/README.md`
2. **Process**: The workflow copies the content to the root `README.md`
3. **Commit**: If changes are detected, it automatically commits and pushes the update
4. **Result**: Your root README stays synchronized with the python-generators README

## Local Testing

You can test the README copying functionality locally using the provided script:

```bash
python3 update_readme.py
```

This will copy the content from `python-generators-0x00/README.md` to the root `README.md` with the same formatting as the advanced workflow.

## Workflow Features

### Automatic Triggers
- **Push Events**: Triggers when `python-generators-0x00/README.md` is modified
- **Manual Dispatch**: Can be triggered manually from GitHub Actions tab
- **Scheduled**: Advanced workflow runs daily at midnight UTC (ensures sync)

### Safety Features
- **Change Detection**: Only commits if actual changes are detected
- **Error Handling**: Fails gracefully if source file doesn't exist
- **Proper Permissions**: Uses appropriate GitHub token permissions

### Commit Messages
- **Basic**: Simple commit message with robot emoji
- **Advanced**: Detailed commit message with context and trigger information

## Setup Requirements

1. **Repository Permissions**: Ensure the workflow has write permissions to the repository
2. **GitHub Token**: Uses `GITHUB_TOKEN` secret (automatically provided)
3. **Branch Protection**: If using branch protection, ensure the workflow can push to the main branch

## Customization

You can modify the workflows to:
- Change the source/target file paths
- Adjust the header content
- Modify the commit message format
- Change the schedule timing
- Add additional processing steps

## Troubleshooting

### Common Issues
1. **Permission Denied**: Check repository settings for workflow permissions
2. **File Not Found**: Ensure the source README file exists
3. **No Changes Detected**: The workflow only commits when actual changes are made

### Manual Override
If the automatic workflow fails, you can:
1. Run the local script: `python3 update_readme.py`
2. Manually trigger the workflow from GitHub Actions tab
3. Manually copy the content and commit

## File Structure

```
.github/
├── workflows/
│   ├── update-readme.yml          # Basic workflow
│   └── update-readme-advanced.yml # Advanced workflow
├── update_readme.py               # Local testing script
├── README.md                      # Auto-generated root README
└── python-generators-0x00/
    └── README.md                  # Source README
``` 