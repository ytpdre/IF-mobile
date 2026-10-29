# InFalsus

In Falsus —— 由 lowiro 开发的 Unity 游戏（Steam / Windows）。本仓库托管项目文档与发布辅助工具；游戏本体通过 [Releases](https://atomgit.com/aztcd/InFalsus/releases) 以分卷压缩包形式分发。

> 本仓库为发布产物分析重建的项目骨架，不包含游戏源码、资源或二进制文件。

## 源码骨架（可编译）

`src/` 下是与 1.0.6 程序集划分对应的 .NET 工程，按模块建库（不含任何游戏逻辑或反编译内容）：

```
src/
├── UnityShim/               # 最小 UnityEngine 兼容垫片，使工程脱离 Unity 也可编译
├── Game.Common/             # 模块公共服务
├── Game.Data/               # 定义数据
├── Game.Audio/              # 音频（真实构建接 FMOD）
├── Game.Input/              # 输入（真实构建接 Unity InputSystem）
├── Game.Character/          # 角色注册
├── Game.NativeTime/         # 时钟抽象
├── Game.NovelEngine/        # 剧情/Novel 引擎入口
├── Game.UI.Common/          # UI 服务
├── Game.Common.Rendering/   # 渲染设置（真实构建接 URP）
└── Game/                    # 组合根，引用以上全部模块
```

编译验证（无需 Unity，任意 .NET 8 SDK 即可）：

```bash
dotnet build src/Game/Game.csproj
```

各模块当前只含模块边界桩（公开入口 + 空实现），用于固化程序集结构与依赖方向；真实的游戏逻辑、资源与第三方库（FMOD、Steamworks.NET、MemoryPack、Obfuz 等）不在本仓库。

## 发布产物结构

当前发布：**1.0.6**（Windows x64，完整客户端，约 6.7 GB / 12230 个文件）。

附件为分卷 zip（`InFalsus.zip.001` ~ `.004`），合并后内含 `In Falsus/` 目录：

```
In Falsus/
├── infalsus.exe                 # 主程序入口
├── GameAssembly.dll             # IL2CPP 编译的游戏代码
├── UnityPlayer.dll              # Unity 运行时
├── UnityCrashHandler64.exe
├── baselib.dll
├── D3D12/D3D12Core.dll
├── Licenses.txt                 # 第三方许可证（字体等）
├── dlc/
│   └── dlc-vsingers-0/sam/      # 内置 DLC：虚拟歌手资源包（~20 MB，25 个文件）
└── infalsus_Data/
    ├── globalgamemanagers*      # 引擎全局设置与场景
    ├── level0
    ├── resources.assets* / sharedassets0.assets*
    ├── il2cpp_data/             # IL2CPP 元数据
    ├── Plugins/                 # steam_api64 等原生插件
    ├── Resources/               # Unity 内置资源
    └── StreamingAssets/
        ├── aa/                  # Addressables catalog 与本地 bundle
        ├── sam/                 # 内置资源包（~5.1 GB，10356 个文件）
        └── UnityServicesProjectConfiguration.json
```

## 下载与运行

1. 从 Releases 下载全部 4 个分卷，置于同一目录。
2. 用 7-Zip / WinRAR / Bandizip 解压 `InFalsus.zip.001`（其余分卷自动合并）。
3. 运行 `In Falsus/infalsus.exe`。

## 技术栈

| 类别 | 组件 |
|---|---|
| 引擎 | Unity 6000.3.9f1（IL2CPP，URP，Burst，Collections，Mathematics） |
| 资源系统 | Unity Addressables + ScriptableBuildPipeline + ResourceManager |
| 输入 | Unity Input System |
| UI | TextMeshPro，Lowiro.UI.Projection |
| 音频 | FMOD（FMODUnity），Game.Audio |
| Steam | Steamworks.NET 2024.8.0（Steamworks SDK 1.60） |
| 序列化 | MemoryPack，Newtonsoft.Json，ZString |
| 安全加固 | Obfuz.Runtime |
| 热重载 | SingularityGroup.HotReload |
| 其他 | Visual Effect Graph，Splines，Timeline，HarfBuzzSharp，FMOD（FastText），Game.NovelEngine 等自研模块 |

游戏代码按模块划分（程序集名）：

```
Game.dll / Game.Audio / Game.Character / Game.Common / Game.Common.Rendering
Game.Data / Game.Input / Game.NativeTime / Game.NovelEngine / Game.UI.Common
```

## 许可

- 仓库自身代码：AGPL-3.0（见 [LICENSE](LICENSE)）。
- 游戏资源与二进制不在本仓库分发，版权归 lowiro 所有。
- 第三方组件许可见包内 `In Falsus/Licenses.txt`（Chiron Hei 字体 SIL OFL 1.1，vivo Sans 自定义许可等）。

## 工具

`tools/` 目录提供发布包分析脚本（不随游戏资源分发）：

- `inspect_release.py` — 流式解析分卷 zip 的目录结构与统计信息，无需完整解压。

```bash
python3 tools/inspect_release.py InFalsus.zip.001 InFalsus.zip.002 InFalsus.zip.003 InFalsus.zip.004
```
