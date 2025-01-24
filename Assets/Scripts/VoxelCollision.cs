using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VoxelCollision : MonoBehaviour
{
    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Voxel"))
        {
            // Destroy or deactivate the voxel
            other.gameObject.SetActive(false);
        }
    }
}
