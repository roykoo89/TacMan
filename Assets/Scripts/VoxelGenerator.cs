using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VoxelGenerator : MonoBehaviour
{
    public GameObject voxelPrefab;       // The voxel prefab
    public GameObject triggerCubePrefab; // The trigger cube prefab (empty GameObject with a trigger collider)
    public int gridSize = 10;            // Number of voxels along each axis
    public float voxelSize = 1f;         // Size of each voxel

    public GameObject grabbableParent;

    // Dictionary to store voxel positions
    public static Dictionary<Vector3Int, GameObject> voxelGrid = new Dictionary<Vector3Int, GameObject>();

    //private BoxCollider voxelParentCollider;

    void Start()
    {
        GenerateVoxels();
        // Ensure the VoxelParent has a BoxCollider
        //voxelParentCollider = gameObject.GetComponent<BoxCollider>();
        SetupGrabbableParent();

        // Adjust the collider to encase all voxels
        //AdjustVoxelParentCollider();
    }

    void GenerateVoxels()
    {
        Vector3 parentPosition = transform.position;

        for (int x = 0; x < gridSize; x++)
        {
            for (int y = 0; y < gridSize; y++)
            {
                for (int z = 0; z < gridSize; z++)
                {
                    Vector3Int gridPosition = new Vector3Int(x, y, z);

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

                        voxelGrid[gridPosition] = triggerCube;

                        // Set grid position in the CollisionHandler
                        var collisionHandler = triggerCube.GetComponent<CollisionHandler>();
                        if (collisionHandler != null)
                        {
                            collisionHandler.gridPosition = gridPosition;
                        }
                    }
                    else
                    {
                        // Instantiate a voxel for the inner grid
                        GameObject voxel = Instantiate(voxelPrefab, position, Quaternion.identity, transform);

                        // Scale the voxel
                        voxel.transform.localScale = Vector3.one * voxelSize;

                        voxelGrid[gridPosition] = voxel;

                        // Set grid position in the CollisionHandler
                        var collisionHandler = voxel.GetComponent<CollisionHandler>();
                        if (collisionHandler != null)
                        {
                            collisionHandler.gridPosition = gridPosition;
                        }
                    }
                }
            }
        }
    }

    void SetupGrabbableParent()
    {
        // Calculate the bounds of the grid
        float gridExtent = (gridSize - 1) * voxelSize;
        Vector3 gridCenter = new Vector3(gridExtent / 2, gridExtent / 2, gridExtent / 2);

        // Add a BoxCollider to the grabbable parent
        BoxCollider boxCollider = grabbableParent.GetComponent<BoxCollider>();
        boxCollider.center = gridCenter;
        boxCollider.size = new Vector3(gridSize, gridSize, gridSize) * voxelSize;
    }

    void AdjustVoxelParentCollider()
    {
        // Calculate the bounds of the entire voxel grid
        Vector3 minBounds = transform.position;
        Vector3 maxBounds = minBounds + new Vector3(gridSize, gridSize, gridSize) * voxelSize;

        // Center of the collider
        Vector3 center = (minBounds + maxBounds) / 2f;

        // Size of the collider
        Vector3 size = maxBounds - minBounds;

        // Adjust the BoxCollider
        //voxelParentCollider.center = transform.InverseTransformPoint(center); // Local center
        //voxelParentCollider.size = size;

        // Ensure the collider is enabled
        //voxelParentCollider.isTrigger = false; // Set to trigger if necessary
    }
}
