using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpawnManager : MonoBehaviour
{
    public GameObject voxelPrefab;
    public GameObject leftHand;
    private GameObject voxelInstance;
    
    public void SpawnSetPositionVoxel()
    {
        if (voxelInstance == null)
        {
            voxelInstance = Instantiate(voxelPrefab, leftHand.transform.position, Quaternion.identity);
        }
        else
        {
            voxelInstance.transform.position = leftHand.transform.position;
        }
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            SpawnSetPositionVoxel();
        }
    }
}
