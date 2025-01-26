using UnityEngine;

public class StickSimulation : MonoBehaviour
{
    //make this instanced
    public static StickSimulation Instance { get; private set; }
    
    public Transform Servo1, Servo2, RotatePt; // Base points
    public Transform Hinge1, Hinge2; // Hinges
    public Transform ConnectionPoint; // Connection point

    public LineRenderer Rod1a, Rod1b, Rod2a, Rod2b; // Rods (LineRenderers)

    public float L1a = 5f, L1b = 10f, L2a = 5f, L2b = 10f; // Rod lengths
    public float Theta1 = 45f, Theta2 = 135f, Phi = 0f; // Angles
    
    private float previousTheta1, previousTheta2, previousPhi; // Previous angles
    
    void Awake()
    {
        // Ensure only one instance of Communicator exists
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject); // Optional: Persist across scenes
        }
        else
        {
            Destroy(gameObject); // Destroy duplicate instances
        }
    }
    void Update()
    {
        // Check if any value has changed
        if (Theta1 != previousTheta1 || Theta2 != previousTheta2 || Phi != previousPhi)
        {
            // Convert angles to radians
            float theta1Rad = Mathf.Deg2Rad * Theta1;
            float theta2Rad = Mathf.Deg2Rad * Theta2;
            float phiRad = Mathf.Deg2Rad * Phi;

            // Calculate hinge positions (2D first)
            Vector3 H1_2D = new Vector3(-L1a * Mathf.Sin(theta1Rad), 0, -L1a * Mathf.Cos(theta1Rad));
            Vector3 H2_2D = new Vector3(-L2a * Mathf.Sin(theta2Rad), 0, -L2a * Mathf.Cos(theta2Rad));

            // Rotate around Y-axis for 3D
            Hinge1.localPosition = H1_2D + Servo1.localPosition;
            Hinge2.localPosition = H2_2D + Servo2.localPosition;

            // Find connection point (intersection of two circles)
            Vector3 connection = FindConnectionPoint(Hinge1.localPosition, L1b, Hinge2.localPosition, L2b);
            ConnectionPoint.localPosition = connection;

            // Rotate the rotate point by phi which is the parent of the servos
            RotatePt.localRotation = Quaternion.Euler(0, 0, Phi);

            // Update rods (LineRenderer positions)
            Rod1a.SetPosition(0, Servo1.position);
            Rod1a.SetPosition(1, Hinge1.position);

            Rod1b.SetPosition(0, Hinge1.position);
            Rod1b.SetPosition(1, ConnectionPoint.position);

            Rod2a.SetPosition(0, Servo2.position);
            Rod2a.SetPosition(1, Hinge2.position);

            Rod2b.SetPosition(0, Hinge2.position);
            Rod2b.SetPosition(1, ConnectionPoint.position);
            // Update previous values
            previousTheta1 = Theta1;
            previousTheta2 = Theta2;
            previousPhi = Phi;
        }
    }

    public void SetAngles(float theta1, float theta2, float phi)
    {
        Theta1 = theta1;
        Theta2 = theta2;
        Phi = phi;
    }
    
    private Vector3 RotateY(Vector3 point, float angle)
    {
        float cos = Mathf.Cos(angle);
        float sin = Mathf.Sin(angle);
        return new Vector3(
            cos * point.x - sin * point.z,
            point.y,
            sin * point.x + cos * point.z
        );
    }
    
    private Vector3 RotateX(Vector3 point, float angle)
    {
        float cos = Mathf.Cos(angle);
        float sin = Mathf.Sin(angle);
        return new Vector3(
            point.x,
            cos * point.y - sin * point.z,
            sin * point.y + cos * point.z
        );
    }
    
    private Vector3 RotateZ(Vector3 point, float angle)
    {
        float cos = Mathf.Cos(angle);
        float sin = Mathf.Sin(angle);
        return new Vector3(
            cos * point.x - sin * point.y,
            sin * point.x + cos * point.y,
            point.z
        );
    }

    private Vector3 FindConnectionPoint(Vector3 center1, float radius1, Vector3 center2, float radius2)
    {
        Vector3 dir = center2 - center1;
        float d = dir.magnitude;

        if (d > radius1 + radius2 || d < Mathf.Abs(radius1 - radius2))
        {
            Debug.LogWarning("No valid connection point!");
            return center1; // Default fallback
        }

        float a = (radius1 * radius1 - radius2 * radius2 + d * d) / (2 * d);
        float h = Mathf.Sqrt(radius1 * radius1 - a * a);

        Vector3 P2 = center1 + dir.normalized * a;
        Vector3 offset = Vector3.Cross(dir.normalized, Vector3.up) * h;

        return P2 + offset; // One of the intersection points
    }
}
