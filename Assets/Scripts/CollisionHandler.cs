using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CollisionHandler : MonoBehaviour
{
    public int valueOnCollision = 0; // Value to send when collided
    public bool isVoxel = false;    // Whether the object is a voxel
    public Vector3Int gridPosition; // The voxel's grid position

    private bool hasDisappeared = false; // Track if the voxel has already disappeared
    private MeshRenderer meshRenderer;
    private Collider objectCollider;

    void Start()
    {
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

            Vector3 collisionNormal = (transform.position - other.transform.position).normalized;

            // Handle voxel behavior
            if (isVoxel && !hasDisappeared)
            {
                //Debug.Log($"Voxel collided: Sending value {valueOnCollision}");
                //Debug.Log($"Neighbor status: {neighborStatus}");
                //Debug.Log(valueOnCollision.ToString() + " " + neighborStatus);
                //ExampleCommunicator.Instance.SendMessageToServer(valueOnCollision.ToString() + " " + neighborStatus);

                GetAndSendSpace(collisionNormal);
                hasDisappeared = true;
                meshRenderer.enabled = false;
                objectCollider.isTrigger = true;
                valueOnCollision = 0;
            }
            else
            {
                //Debug.Log(valueOnCollision.ToString() + " " + neighborStatus);
                //ExampleCommunicator.Instance.SendMessageToServer(valueOnCollision.ToString() + " " + neighborStatus);
            }
        }
    }

    void GetAndSendSpace(Vector3 collisionNormal)
    {
        // Define face normals for comparison
        Vector3[] faceNormals = {
            new Vector3(1, 0, 0),  // Right
            new Vector3(-1, 0, 0), // Left
            new Vector3(0, 1, 0),  // Top
            new Vector3(0, -1, 0), // Bottom
            new Vector3(0, 0, 1),   // Front
            new Vector3(0, 0, -1) // Back
    };

        string[] faceNames = { "4", "5", "6", "1", "2", "3" };

        // Determine which face was hit
        float maxDot = -1f;
        int closestFaceIndex = -1;

        for (int i = 0; i < faceNormals.Length; i++)
        {
            // Compute the dot product between collision normal and face normal
            float dot = Vector3.Dot(collisionNormal, faceNormals[i]);

            // Find the closest face (largest dot product)
            if (dot > maxDot)
            {
                maxDot = dot;
                closestFaceIndex = i;
            }
        }

        if (closestFaceIndex != -1)
        {
            // Get the name of the face that was hit
            string hitFace = faceNames[closestFaceIndex];

            // Send information to the communicator
            Debug.Log($"{hitFace}");
            ExampleCommunicator.Instance?.SendMessageToServer($"{hitFace}");
        }
        else
        {
            Debug.LogWarning("No face detected. Collision normal might be invalid.");
        }
    }

    string GetNeighborStatus()
    {
        // Neighbor offsets for Left, Top, Right, Bottom, Front, Back
        Vector3Int[] neighborOffsets = new Vector3Int[]
        {
            new Vector3Int(1, 0, 0),  // Right
            new Vector3Int(-1, 0, 0), // Left            
            new Vector3Int(0, 1, 0),  // Top
            new Vector3Int(0, -1, 0), // Bottom
            new Vector3Int(0, 0, 1),  // Front
            new Vector3Int(0, 0, -1)  // Back
        };

        string status = "";

        foreach (var offset in neighborOffsets)
        {
            Vector3Int neighborPosition = gridPosition + offset;

            // Check if the neighbor exists in the grid
            if (VoxelGenerator.voxelGrid.ContainsKey(neighborPosition))
            {
                GameObject neighbor = VoxelGenerator.voxelGrid[neighborPosition];
                var neighborHandler = neighbor.GetComponent<CollisionHandler>();

                // Check if the neighbor has disappeared
                status += neighborHandler != null && !neighborHandler.hasDisappeared ? "1" : "0";
            }
            else
            {
                // No neighbor exists
                status += "0";
            }

            status += ",";
        }

        return status.TrimEnd(',');
    }
}