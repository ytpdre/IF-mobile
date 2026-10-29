// Minimal compile-time shim of the Unity APIs used by the skeleton.
// NOT the real Unity engine — real builds use the Unity editor's reference assemblies.
using System;

namespace UnityEngine
{
    public class Object { }
    public class Component : Object { }
    public class Behaviour : Component { }
    public class MonoBehaviour : Behaviour { }
    public class ScriptableObject : Object { }

    public struct Vector2 { public float x, y; public Vector2(float x, float y) { this.x = x; this.y = y; } }
    public struct Vector3 { public float x, y, z; public Vector3(float x, float y, float z) { this.x = x; this.y = y; this.z = z; } }
    public struct Quaternion { public float x, y, z, w; }

    public class GameObject : Object
    {
        public string name { get; set; }
        public GameObject(string name = "") { this.name = name; }
    }

    public class Transform : Component { }

    public enum LogLevel { Info, Warning, Error }

    public static class Debug
    {
        public static event Action<string, LogLevel> LogHandler;
        public static void Log(object message) => LogHandler?.Invoke(message?.ToString() ?? "", LogLevel.Info);
        public static void LogWarning(object message) => LogHandler?.Invoke(message?.ToString() ?? "", LogLevel.Warning);
        public static void LogError(object message) => LogHandler?.Invoke(message?.ToString() ?? "", LogLevel.Error);
    }

    [AttributeUsage(AttributeTargets.Field)]
    public sealed class SerializeField : Attribute { }

    [AttributeUsage(AttributeTargets.Class)]
    public sealed class CreateAssetMenuAttribute : Attribute
    {
        public string menuName;
        public string fileName;
    }
}

namespace Unity.Collections
{
    // Placeholder for Unity.Collections types referenced by the module layout.
    public struct NativeArray<T> : IDisposable
    {
        public void Dispose() { }
    }
}
