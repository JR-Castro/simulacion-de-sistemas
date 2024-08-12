package ar.edu.itba.ss.models;

import static java.lang.Math.pow;

public class Particle {
    private double x;
    private double y;
    private double radius;
    private double property;

    public Particle(double x, double y, double radius, double property) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.property = property;
    }

    public double distanceTo(Particle q) {
        return Math.sqrt(pow((x - q.x), 2) + pow((y - q.y), 2));
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public double getRadius() {
        return radius;
    }

    public void setX(double x) {
        this.x = x;
    }

    public void setY(double y) {
        this.y = y;
    }

    public void setRadius(double radius) {
        this.radius = radius;
    }

    public double getProperty() {
        return property;
    }

    public void setProperty(double property) {
        this.property = property;
    }
}
