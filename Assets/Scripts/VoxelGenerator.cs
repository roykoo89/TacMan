using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VoxelGenerator : MonoBehaviour
{
    public GameObject voxelPrefab;       // The voxel prefab
    public GameObject triggerCubePrefab; // The trigger cube prefab (empty GameObject with a trigger collider)
    public int gridSize = 10;            // Number of voxels along each axis
    public float voxelSize = 1f;         // Size of each voxel

    void Start()
    {
        GenerateVoxels();
    }

    void GenerateVoxels()
    {
        // Get the starting position from the VoxelParent's position
        Vector3 parentPosition = transform.position;

        for (int x = 0; x < gridSize; x++)
        {
            for (int y = 0; y < gridSize; y++)
            {
                for (int z = 0; z < gridSize; z++)
                {
                    // Calculate the position of each cube relative to the parent
                    Vector3 position = parentPosition + new Vector3(x, y, z) * voxelSize;

                    // Check if the current position is part of the outer layer
                    if (x == 0 || x == gridSize - 1 ||
                        y == 0 || y == gridSize - 1 ||
                        z == 0 || z == gridSize - 1)
                    {
                        // Instantiate a trigger cube for the outer layer
                        GameObject triggerCube = Instantiate(triggerCubePrefab, position, Quaternion.identity, transform);

                        // Scale the trigger cube
                        triggerCube.transform.localScale = Vector3.one * voxelSize;
                    }
                    else
                    {
                        // Instantiate a voxel for the inner grid
                        GameObject voxel = Instantiate(voxelPrefab, position, Quaternion.identity, transform);

                        // Scale the voxel
                        voxel.transform.localScale = Vector3.one * voxelSize;
                    }
                }
            }
        }
    }
}
