#!/bin/bash
# 每日自动整理交互记录文件夹
# 归档截图到日期子目录，删除临时文件

DIR="/Users/libo/Desktop/claude code/04-交互记录"
TODAY=$(date +%Y-%m-%d)
ARCHIVE="$DIR/归档/$TODAY"

mkdir -p "$ARCHIVE"

for f in "$DIR"/*; do
    [ -e "$f" ] || continue
    name=$(basename "$f")

    # 跳过的目录
    [ -d "$f" ] && continue

    # 删除临时/处理过的文件
    case "$name" in
        shot_*.jpg|shot_*.png)
            rm -f "$f"
            ;;
        ScreenShot_*)
            mv "$f" "$ARCHIVE/"
            ;;
        *.png|*.jpg|*.jpeg)
            mv "$f" "$ARCHIVE/"
            ;;
    esac
done

echo "交互记录已整理: $ARCHIVE"
