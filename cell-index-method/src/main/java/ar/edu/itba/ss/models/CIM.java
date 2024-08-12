package ar.edu.itba.ss.models;

import java.util.*;
import java.util.function.Function;

public class CIM {
    private final double l;
    private final List<Particle> particles;
    private final double r;
    private final int m;

    private static final Function<Integer, Set<Integer>> SET_INSTANTIATOR = x -> new HashSet<>();

    public CIM(Context context) {
        this.l = context.getLength();
        this.particles = context.getParticles();
        this.r = context.getInteractionRadius();
        this.m = context.getMatrixSize();
    }

    public Map<Integer, Set<Integer>> compute() {
        Cell[][] particlesInGrid = new Cell[m][m];
        int c;
        final Map<Integer, Set<Integer>> result = new HashMap<>();

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                particlesInGrid[i][j] = new Cell();
            }
        }

        for (int i = 0; i < particles.size(); i++) {
            c = whereIsParticle(particles.get(i));
            particlesInGrid[c / m][c % m].addParticle(i);
        }

        for (int i = 0; i < particles.size(); i++) {
            c = whereIsParticle(particles.get(i));
            int ii = c / m;
            int iii = c % m;
            int finalI = i;

            Set<Integer> neightborList = result.computeIfAbsent(finalI, SET_INSTANTIATOR);
            particlesInGrid[ii][iii].getParticles().forEach(iv -> {
                if (finalI != iv && particles.get(finalI).distanceTo(particles.get(iv)) <= r) {
                    neightborList.add(iv);
                    result.computeIfAbsent(iv, SET_INSTANTIATOR).add(finalI);
                }
            });
            if (ii < m - 1) {
                particlesInGrid[c / m + 1][c % m].getParticles().forEach((iv) -> {
                    if (finalI != iv && particles.get(finalI).distanceTo(particles.get(iv)) <= r) {
                        neightborList.add(iv);
                        result.computeIfAbsent(iv, SET_INSTANTIATOR).add(finalI);
                    }
                });
                if (iii < m - 1) {
                    particlesInGrid[c / m + 1][c % m + 1].getParticles().forEach((iv) -> {
                        if (finalI != iv && particles.get(finalI).distanceTo(particles.get(iv)) <= r) {
                            neightborList.add(iv);
                            result.computeIfAbsent(iv, SET_INSTANTIATOR).add(finalI);
                        }
                    });
                }
            }
            if (iii < m - 1) {
                particlesInGrid[c / m + 1][c % m + 1].getParticles().forEach((iv) -> {
                    if (finalI != iv && particles.get(finalI).distanceTo(particles.get(iv)) <= r) {
                        neightborList.add(iv);
                        result.computeIfAbsent(iv, SET_INSTANTIATOR).add(finalI);
                    }
                });
                if (ii > 0) {
                    particlesInGrid[c / m - 1][c % m + 1].getParticles().forEach((iv) -> {
                        if (finalI != iv && particles.get(finalI).distanceTo(particles.get(iv)) <= r) {
                            neightborList.add(iv);
                            result.computeIfAbsent(iv, SET_INSTANTIATOR).add(finalI);
                        }
                    });
                }
            }
        }

        return result;
    }

    private int whereIsParticle(Particle p) {
        int i = (int) Math.floor(p.getY() / (l / m));
        int j = (int) Math.floor(p.getX() / (l / m));

        return i * m + j;
    }
}