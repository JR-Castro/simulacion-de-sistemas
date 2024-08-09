package ar.edu.itba.ss;

import java.util.ArrayList;
import java.util.List;

public class Cell {
    private final List<Integer> particles;

    public Cell() {
        this.particles = new ArrayList<>();
    }

    public void addParticle(int i) {
        particles.add(i);
    }

    public List<Integer> getParticles() {
        return particles;
    }
}
