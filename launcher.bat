@echo off 
if exist "eliza.py" (
    if exist "main.py" (
        python main.py
    ) else (
    echo ...
    )
) else (
    echo ...
)
