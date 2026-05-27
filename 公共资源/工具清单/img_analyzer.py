"""AI图片质量分析工具 （纯PIL版）"""
import sys
import json
from PIL import Image, ImageStat, ImageFilter

def analyze(image_path):
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    # 清晰度：边缘检测后统计方差
    edges = img.filter(ImageFilter.FIND_EDGES)
    edge_stat = ImageStat.Stat(edges)
    sharpness = sum(edge_stat.var) / 3

    # 亮度
    stat = ImageStat.Stat(img)
    mean_r, mean_g, mean_b = stat.mean
    brightness = (mean_r + mean_g + mean_b) / 3
    std_r, std_g, std_b = stat.stddev
    color_richness = (std_r + std_g + std_b) / 3

    # 判断
    issues = []
    warnings = []

    if sharpness < 30:
        issues.append("严重模糊")
    elif sharpness < 60:
        warnings.append("清晰度偏低")
    elif sharpness > 250:
        warnings.append("可能锐化过度")

    if brightness < 30:
        issues.append("严重偏暗")
    elif brightness < 55:
        warnings.append("偏暗")
    elif brightness > 230:
        issues.append("严重过曝")
    elif brightness > 210:
        warnings.append("偏亮")

    if color_richness < 15:
        warnings.append("色彩单一")

    if issues:
        grade = "C"
    elif len(warnings) >= 2:
        grade = "B"
    elif warnings:
        grade = "B+"
    else:
        grade = "A"

    return {
        "文件": image_path.split("/")[-1],
        "尺寸": f"{w}x{h}",
        "清晰度": f"{sharpness:.0f}",
        "亮度": f"{brightness:.0f}",
        "色彩": f"{color_richness:.0f}",
        "问题": issues if issues else "无",
        "提醒": warnings if warnings else "无",
        "等级": grade,
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 img_analyzer.py 图片路径 [图片路径...]")
        sys.exit(1)

    for path in sys.argv[1:]:
        try:
            result = analyze(path)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print("---")
        except Exception as e:
            print(f"X {path}: {e}")
