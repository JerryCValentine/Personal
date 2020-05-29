using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MathCalculator : MonoBehaviour
{
    [SerializeField]
    List<Vector2> function = new List<Vector2>();
    [SerializeField]
    List<Vector2> firstDerivitive = new List<Vector2>();
    [SerializeField]
    List<Vector2> secondDerivitive = new List<Vector2>();
    [SerializeField]
    List<Vector2> antiDerivitive = new List<Vector2>();
    public float intergralArea;
    private Vector3[] arcArray;
    private double[,] matrixA;
    private double[] matrixB;
    private double[,] matrixAdj;
    private double T1;
    private double T2;
    private double T3;
    private double T4;
    private double alpha;
    private double MatrixMod;
    private double C1;
    private double C2;
    private double C3;

    public static bool runMatrix = false;

    public void Start()
    {
        //function.Clear();
        firstDerivitive.Clear();
        secondDerivitive.Clear();

        firstDerivitive = TakeDerivitive(function);
        secondDerivitive = TakeDerivitive(firstDerivitive);
        intergralArea = FindIntergralArea(function, 0, 3);

        matrixA = new double[3, 3];
        matrixAdj = new double[4, 4];
        matrixB = new double[3];
    }

    /*
    public void Update()
    {
        //arcArray = LaunchArcRender.arcArray;

        if (runMatrix)
        {
            LoadMatrixA();
            LoadMatrixB();
            LoadMatrixAdj();
            FindAMod();
            AdjustMatrixA();
            FindCoe();
            runMatrix = false;
        }
    }
    */

    public MathCalculator(double a, double b, double c)
    {
        function.Clear();
        function.Add(new Vector2((float)a, 2));
        function.Add(new Vector2((float)b, 1));
        function.Add(new Vector2((float)c, 0));
    }

    public MathCalculator(double a, double b)
    {
        function.Clear();
        function.Add(new Vector2((float)a, 1));
        function.Add(new Vector2((float)b, 0));
    }

    public List<Vector2> TakeDerivitive(List<Vector2> function)
    {
        List<Vector2> derivitive = new List<Vector2>();
        double coe;
        double exp;

        derivitive.Clear();

        for (int i = 0; i < function.ToArray().Length - 1; ++i)
        {
            coe = function[i].x * function[i].y;
            exp = function[i].y - 1;
            if (exp == -1)
                exp = 0;
            derivitive.Add(new Vector2((float)coe, (float)exp));
        }

        return derivitive;
    }

    public float FindIntergralArea(List<Vector2> funciton, float lowBound, float highBound)
    {
        antiDerivitive = TakeAntiDerivitive(funciton);

        return PlugInBounds(antiDerivitive, lowBound, highBound);
    }

    public List<Vector2> TakeAntiDerivitive(List<Vector2> function)
    {
        List<Vector2> antiDerivitive = new List<Vector2>();
        double exp;
        double coe;

        antiDerivitive.Clear();

        for (int i = 0; i < function.ToArray().Length; ++i)
        {
            exp = function[i].y + 1;
            coe = function[i].x / exp;
            antiDerivitive.Add(new Vector2((float)coe, (float)exp));
        }

        return antiDerivitive;
    }

    public float PlugInBounds(List<Vector2> antiDerivitive, float lowBound, float highBound)
    {
        float resultA;
        float resultB;

        resultA = SolveY(lowBound, antiDerivitive);
        resultB = SolveY(highBound, antiDerivitive);

        return (resultA - resultB);
    }

    public float SolveY(float x, List<Vector2> function)
    {
        double result = 0;

        for (int i = 0; i < function.ToArray().Length; ++i)
        {
            result += (Mathf.Pow(x, function[i].y) * function[i].x);
        }

        return (float)result;
    }

    /*
    private void LoadMatrixA()
    {
        T1 = 0;
        T2 = 0;
        T3 = 0;
        T4 = 0;

        foreach (Vector3 value in arcArray)
        {
            T1 += value.x;
        }

        foreach (Vector3 value in arcArray)
        {
            T2 += Mathf.Pow(value.x, 2);
        }

        foreach (Vector3 value in arcArray)
        {
            T3 += Mathf.Pow(value.x, 3);
        }

        foreach (Vector3 value in arcArray)
        {
            T4 += Mathf.Pow(value.x, 3);
        }

        matrixA[2, 0] = arcArray.Length;
        matrixA[2, 1] = T1;
        matrixA[2, 2] = T2;
        matrixA[1, 0] = T1;
        matrixA[1, 1] = T2;
        matrixA[1, 2] = T3;
        matrixA[0, 0] = T2;
        matrixA[0, 1] = T3;
        matrixA[0, 2] = T4;
    }

    private void LoadMatrixB()
    {
        alpha = 0;

        foreach (Vector3 item in arcArray)
        {
            alpha += item.y;
        }

        matrixB[0] = alpha;
        matrixB[1] = alpha * T1;
        matrixB[2] = alpha * T2;
    }

    private void FindAMod()
    {
        double x = 0;
        double y = 0;

        x += (matrixA[2, 0] * matrixA[1, 1] * matrixA[0, 2]);
        x += (matrixA[2, 1] * matrixA[1, 2] * matrixA[0, 0]);
        x += (matrixA[2, 2] * matrixA[1, 0] * matrixA[0, 1]);

        y += (matrixA[0, 0] * matrixA[1, 1] * matrixA[2, 2]);
        y += (matrixA[0, 1] * matrixA[1, 2] * matrixA[2, 0]);
        y += (matrixA[0, 2] * matrixA[1, 0] * matrixA[2, 1]);

        MatrixMod = y - x;
    }

    private void LoadMatrixAdj()
    {
        matrixAdj[0, 0] = matrixA[1, 1];
        matrixAdj[0, 1] = matrixA[1, 2];
        matrixAdj[0, 2] = matrixA[1, 0];
        matrixAdj[0, 3] = matrixA[1, 1];
        matrixAdj[1, 0] = matrixA[2, 1];
        matrixAdj[1, 1] = matrixA[2, 2];
        matrixAdj[1, 2] = matrixA[2, 0];
        matrixAdj[1, 3] = matrixA[2, 1];
        matrixAdj[2, 0] = matrixA[0, 1];
        matrixAdj[2, 1] = matrixA[0, 2];
        matrixAdj[2, 2] = matrixA[0, 0];
        matrixAdj[2, 3] = matrixA[0, 1];
        matrixAdj[3, 0] = matrixA[1, 1];
        matrixAdj[3, 1] = matrixA[1, 2];
        matrixAdj[3, 2] = matrixA[1, 0];
        matrixAdj[3, 3] = matrixA[1, 1];
    }

    private void AdjustMatrixA()
    {
        matrixA[2, 0] = (matrixAdj[3, 0] * matrixAdj[2, 1]) - (matrixAdj[2, 0] * matrixAdj[3, 1]);
        matrixA[2, 1] = (matrixAdj[2, 0] * matrixAdj[1, 1]) - (matrixAdj[1, 0] * matrixAdj[2, 1]);
        matrixA[2, 2] = (matrixAdj[1, 0] * matrixAdj[0, 1]) - (matrixAdj[0, 0] * matrixAdj[1, 1]);
        matrixA[1, 0] = (matrixAdj[3, 1] * matrixAdj[2, 2]) - (matrixAdj[2, 1] * matrixAdj[3, 2]);
        matrixA[1, 1] = (matrixAdj[2, 1] * matrixAdj[1, 2]) - (matrixAdj[1, 1] * matrixAdj[2, 2]);
        matrixA[1, 2] = (matrixAdj[1, 1] * matrixAdj[0, 2]) - (matrixAdj[0, 1] * matrixAdj[1, 2]);
        matrixA[0, 0] = (matrixAdj[3, 2] * matrixAdj[2, 3]) - (matrixAdj[2, 2] * matrixAdj[3, 3]);
        matrixA[0, 1] = (matrixAdj[2, 2] * matrixAdj[1, 3]) - (matrixAdj[1, 2] * matrixAdj[2, 3]);
        matrixA[0, 2] = (matrixAdj[0, 3] * matrixAdj[1, 2]) - (matrixAdj[0, 2] * matrixAdj[0, 3]);

        for (int x = 0; x < matrixA.GetLength(0); x++)
        {
            for (int y = 0; y < matrixA.GetLength(1); y++)
            {
                matrixA[x, y] = matrixA[x, y] * (1 / MatrixMod);
            }
        }
    }

    private void FindCoe()
    {
        C1 = (matrixA[2, 0] * matrixB[0]) + (matrixA[2, 1] * matrixB[1]) + (matrixA[2, 2] * matrixB[2]);
        C2 = (matrixA[1, 0] * matrixB[0]) + (matrixA[1, 1] * matrixB[1]) + (matrixA[1, 2] * matrixB[2]);
        C3 = (matrixA[0, 0] * matrixB[0]) + (matrixA[0, 1] * matrixB[1]) + (matrixA[0, 2] * matrixB[2]);

        Debug.Log(C1);
        Debug.Log(C2);
        Debug.Log(C3);
    }
    */
}
