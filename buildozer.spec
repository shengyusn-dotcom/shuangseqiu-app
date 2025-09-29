[app]

# 应用名称
title = 双色球模拟器

# 包名 (必须唯一，通常用倒置域名)
package.name = shuangseqiu

# 域名
package.domain = org.example

# 源代码目录
source.dir = .

# 主程序文件
source.main = 双色球安卓版.py

# 包含的文件类型
source.include_exts = py,png,jpg,kv,atlas,txt

# 依赖要求
requirements = python3, kivy

# 应用版本
version = 1.0

# 屏幕方向 (portrait-竖屏, landscape-横屏, all-全部)
orientation = portrait

# 是否全屏
fullscreen = 0

# Android权限
android.permissions = INTERNET

# 目标Android API
android.api = 33

# 最低支持的Android版本
android.minapi = 21

# 使用的NDK版本
android.ndk = 25b

# 使用的SDK版本
android.sdk = 28

# 自动接受SDK许可
android.accept_sdk_license = True

# 日志级别
log_level = 2

# 构建目录
build_dir = .buildozer

# 输出目录
bin_dir = bin

#
# OSX Specific
#

#
# author = © Copyright Info

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1