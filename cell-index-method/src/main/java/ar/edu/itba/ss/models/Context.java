package ar.edu.itba.ss.models;

import java.util.List;

public class Context {
    private double length;
    private double interactionRadius;
    private int matrixSize;
    private List<Particle> particles;
    private boolean periodic;

    public Context(double length, double interactionRadius, int matrixSize, List<Particle> particles, boolean periodic) {
        this.length = length;
        this.interactionRadius = interactionRadius;
        this.matrixSize = matrixSize;
        this.particles = particles;
        this.periodic = periodic;
    }

    public double getLength() {
        return length;
    }

    public void setLength(double length) {
        this.length = length;
    }

    public double getInteractionRadius() {
        return interactionRadius;
    }

    public void setInteractionRadius(double interactionRadius) {
        this.interactionRadius = interactionRadius;
    }

    public int getMatrixSize() {
        return matrixSize;
    }

    public void setMatrixSize(int matrixSize) {
        this.matrixSize = matrixSize;
    }

    public List<Particle> getParticles() {
        return particles;
    }

    public void setParticles(List<Particle> particles) {
        this.particles = particles;
    }

    public boolean isPeriodic() {
        return periodic;
    }

    public void setPeriodic(boolean periodic) {
        this.periodic = periodic;
    }
}
