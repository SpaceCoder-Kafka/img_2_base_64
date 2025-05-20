# 图片转 Base64 工具

这个 Python 脚本用于将指定目录下的所有图片文件转换为 Base64 编码，并生成一个 Dart 文件，其中包含所有图片的 Base64 编码字符串。

## 功能特点

- 支持多种常见图片格式（JPG、PNG、GIF、BMP、WebP）
- 递归扫描指定目录及其所有子目录
- 生成符合 Dart 语法的映射表
- 显示处理进度
- 统一的路径分隔符处理
- 完善的错误处理

## 系统要求

- Python 3.6 或更高版本
- 无需额外的第三方依赖

## 使用方法

1. 确保脚本具有执行权限：
   ```bash
   chmod +x img_to_base64.py
   ```

2. 运行脚本：
   ```bash
   ./img_to_base64.py <图片目录路径> [--output 输出文件名]
   ```

   或者使用 Python 直接运行：
   ```bash
   python3 img_to_base64.py <图片目录路径> [--output 输出文件名]
   ```

### 参数说明

- `<图片目录路径>`：必需参数，指定要扫描的图片目录
- `--output` 或 `-o`：可选参数，指定输出的 Dart 文件名（默认为 `base64_images.dart`）

### 示例

```bash
# 扫描当前目录下的所有图片
./img_to_base64.py .

# 扫描指定目录并指定输出文件名
./img_to_base64.py /path/to/images --output my_images.dart
```

## 输出文件

脚本会在指定的目录下生成一个 Dart 文件，其中包含一个名为 `base64Images` 的常量映射表。在 Dart/Flutter 项目中，您可以这样使用它：

```dart
import 'path/to/base64_images.dart';

// 使用示例
final imageBase64 = base64Images['images/logo.png'];
```

## 注意事项

1. 生成的 Dart 文件可能较大，请确保您的项目能够处理大文件
2. 建议在版本控制系统中忽略生成的 Dart 文件
3. 处理大量图片时可能需要较长时间，请耐心等待
4. 所有图片路径都会使用正斜杠（/）作为分隔符，以确保跨平台兼容性 