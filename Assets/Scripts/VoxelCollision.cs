using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VoxelCollision : MonoBehaviour
{
    [SerializeField] private ExampleCommunicator _exampleCommunicator;
    
    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Voxel"))
        {
            // Destroy or deactivate the voxel
            other.gameObject.SetActive(false);
            _exampleCommunicator.SendMessageToServer("ResistMe");
        }
    }
}
