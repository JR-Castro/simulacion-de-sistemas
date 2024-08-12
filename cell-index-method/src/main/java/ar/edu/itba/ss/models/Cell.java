package ar.edu.itba.ss.models;

import java.util.TreeSet;

public class Cell {
    private final TreeSet<Integer> particles;

    public Cell() {
        this.particles = new TreeSet<>();
    }

    public void addParticle(int i) {
        particles.add(i);
    }

    public TreeSet<Integer> getParticles() {
        return particles;
    }
}
