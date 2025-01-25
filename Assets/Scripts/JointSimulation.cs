using UnityEngine;

public class JointSimulation : MonoBehaviour
{
    public Transform Servo1, Servo2;
    public Transform Hinge1, Hinge2;
    public Transform ConnectionPoint;

    public LineRenderer Rod1a, Rod1b, Rod2a, Rod2b;

    public float L1a = 5f, L1b = 10f, L2a = 5f, L2b = 10f;
    public float Theta1 = 45f, Theta2 = 135f, Phi = 0f;

    public float moveSpeed = 2f;  // Keyboard movement speed

    private void Update()
    {
        // Move the connection point using keyboard inputs
        MoveConnectionPoint();

        // Update the hinges and servos based on the connection point
        UpdateHingesAndServos();

        // Update LineRenderers (rods) to keep the distance fixed
        UpdateRodPositions();
    }

    // Move the connection point based on keyboard input (WASD/Arrow keys)
    private void MoveConnectionPoint()
    {
        float moveX = Input.GetAxis("Horizontal") * moveSpeed * Time.deltaTime;
        float moveY = Input.GetAxis("Vertical") * moveSpeed * Time.deltaTime;
        float moveZ = 0f;

        if (Input.GetKey(KeyCode.Q)) moveZ = -moveSpeed * Time.deltaTime; // Move up
        if (Input.GetKey(KeyCode.E)) moveZ = moveSpeed * Time.deltaTime;  // Move down

        // Apply movement to the connection point
        ConnectionPoint.position += new Vector3(moveX, moveY, moveZ);
    }

    // Update the hinges and servos based on the connection point
    private void UpdateHingesAndServos()
    {
        // Calculate the direction from Servo1 to ConnectionPoint (fixed distance)
        Vector3 dir1 = ConnectionPoint.position - Servo1.position;
        dir1 = dir1.normalized * L1a;  // Ensure the length is fixed

        // Calculate the direction from Servo2 to ConnectionPoint (fixed distance)
        Vector3 dir2 = ConnectionPoint.position - Servo2.position;
        dir2 = dir2.normalized * L2a;  // Ensure the length is fixed

        // Set Hinge positions (they should move to accommodate the connection point)
        Hinge1.position = Servo1.position + dir1;
        Hinge2.position = Servo2.position + dir2;

        // If you want to adjust servo rotations based on hinge positions:
        Theta1 = Mathf.Atan2(dir1.y, dir1.x) * Mathf.Rad2Deg;
        Theta2 = Mathf.Atan2(dir2.y, dir2.x) * Mathf.Rad2Deg;

        // Apply rotations to the servos to match hinge positions (simple rotation around Y-axis)
        Servo1.rotation = Quaternion.Euler(0, Theta1, 0);
        Servo2.rotation = Quaternion.Euler(0, Theta2, 0);
    }

    // Update the positions of the rods (LineRenderers)
    private void UpdateRodPositions()
    {
        // Rod 1a (Servo1 to Hinge1)
        Rod1a.SetPosition(0, Servo1.position);
        Rod1a.SetPosition(1, Hinge1.position);

        // Rod 1b (Hinge1 to ConnectionPoint)
        Rod1b.SetPosition(0, Hinge1.position);
        Rod1b.SetPosition(1, ConnectionPoint.position);

        // Rod 2a (Servo2 to Hinge2)
        Rod2a.SetPosition(0, Servo2.position);
        Rod2a.SetPosition(1, Hinge2.position);

        // Rod 2b (Hinge2 to ConnectionPoint)
        Rod2b.SetPosition(0, Hinge2.position);
        Rod2b.SetPosition(1, ConnectionPoint.position);
    }
}
