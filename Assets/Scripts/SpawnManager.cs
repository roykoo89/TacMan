using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpawnManager : MonoBehaviour
{
    public GameObject voxelPrefab;
    public GameObject leftHand;
    
    public void SpawnVoxel()
    {
        Instantiate(voxelPrefab, leftHand.transform.position, Quaternion.identity);
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            SpawnVoxel();
        }
    }
}
