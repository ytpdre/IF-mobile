// Skeleton stub — composition root only, no game logic.
using Game.Common;

namespace Game
{
    /// <summary>Composition root wiring all Game.* modules.</summary>
    public static class GameRoot
    {
        public static void Boot()
        {
            GameServices.Initialize();
            UnityEngine.Debug.Log("[Game] booted (skeleton build)");
        }
    }
}
