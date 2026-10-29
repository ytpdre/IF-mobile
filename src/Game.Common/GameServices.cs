// Skeleton stub — module boundary only, no game logic.
using UnityEngine;

namespace Game.Common
{
    /// <summary>Module-wide services shared by all Game.* assemblies.</summary>
    public static class GameServices
    {
        public static bool Initialized { get; private set; }

        public static void Initialize()
        {
            Debug.Log("[Game.Common] services initialized");
            Initialized = true;
        }
    }
}
