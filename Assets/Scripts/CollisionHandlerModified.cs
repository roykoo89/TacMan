using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CollisionHandlerModified : MonoBehaviour
{
    public Vector3Int gridPosition; // The voxel's grid position

    private Collider objectCollider;

    void Start()
    {
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

            GetAndSendSpace(collisionNormal);
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
            ExampleCommunicator.Instance?.OnCollisionSendOnce($"{hitFace}");
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