package ar.edu.itba.ss;

import static java.lang.Math.*;

public class Position {
    private double x;
    private double y;

    public Position(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double distanceTo(Position q) {
        return Math.sqrt(pow((x - q.x), 2) + pow((y - q.y), 2));
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }
}