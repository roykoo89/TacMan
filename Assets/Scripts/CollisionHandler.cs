using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CollisionHandler : MonoBehaviour
{
    public int valueOnCollision = 0; // The value to send when collided

    // Whether the object is a voxel (can "disappear" on first collision)
    public bool isVoxel = false;

    private bool hasDisappeared = false; // Track if the voxel has already disappeared

    private MeshRenderer meshRenderer;
    private Collider objectCollider;

    void Start()
    {
        // Cache references to components
        meshRenderer = GetComponent<MeshRenderer>();
        objectCollider = GetComponent<Collider>();
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Stick"))
        {
            if (ExampleCommunicator.Instance == null)
            {
                Debug.LogError("Communicator instance is missing!");
                return;
            }

            // Handle voxel behavior
            if (isVoxel && !hasDisappeared)
            {
                // Send value 1 on first collision
                Debug.Log($"Voxel collided: Sending value {valueOnCollision}");
                ExampleCommunicator.Instance.SendMessageToServer("ResistMe");

                // Make the voxel disappear
                hasDisappeared = true;
                meshRenderer.enabled = false; // Disable mesh renderer to make it invisible
                objectCollider.isTrigger = true; // Change to trigger collider
                valueOnCollision = 0; // Set future collision value to 0
            }
            else
            {
                // Handle regular collision
                Debug.Log($"Trigger cube collided: Sending value {valueOnCollision}");
            }
        }
    }
}
