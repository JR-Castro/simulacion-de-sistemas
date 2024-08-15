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

    public int calculateCellIdx(double pos) {
        return (int) (pos / (m * l));
    }

    public Map<Integer, Set<Integer>> compute() {
        Cell[][] particlesInGrid = new Cell[m][m];
        final Map<Integer, Set<Integer>> result = new HashMap<>();

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                particlesInGrid[i][j] = new Cell();
            }
        }

        for (int i = 0; i < particles.size(); i++) {
            Particle particle = particles.get(i);
            particlesInGrid[calculateCellIdx(particle.getY())][calculateCellIdx(particle.getX())].addParticle(i);
        }

        for (int particleIdx = 0; particleIdx < particles.size(); particleIdx++) {
            Particle currentParticle = particles.get(particleIdx);
            int iMatrix = calculateCellIdx(currentParticle.getY());
            int jMatrix = calculateCellIdx(currentParticle.getX());

            Set<Integer> neighborList = result.computeIfAbsent(particleIdx, SET_INSTANTIATOR);

            calculateNeighborsCell(particlesInGrid[iMatrix][jMatrix].getParticles(), particleIdx, neighborList, result);

            if (0 < iMatrix) {
                calculateNeighborsCell(particlesInGrid[iMatrix - 1][jMatrix].getParticles(), particleIdx, neighborList, result);
            }
            if (iMatrix < m - 1) {
                calculateNeighborsCell(particlesInGrid[iMatrix + 1][jMatrix].getParticles(), particleIdx, neighborList, result);
            }
            if (jMatrix < m - 1) {
                calculateNeighborsCell(particlesInGrid[iMatrix][jMatrix + 1].getParticles(), particleIdx, neighborList, result);
            }
            if (iMatrix < m - 1 && jMatrix < m - 1) {
                calculateNeighborsCell(particlesInGrid[iMatrix + 1][jMatrix + 1].getParticles(), particleIdx, neighborList, result);
            }
        }

        return result;
    }

    private void calculateNeighborsCell(TreeSet<Integer> cellParticles, int mainParticleIdx, Set<Integer> neighborList, Map<Integer, Set<Integer>> result) {
        for (int cellParticleIdx : cellParticles) {
            if (mainParticleIdx != cellParticleIdx && particles.get(mainParticleIdx).distanceTo(particles.get(cellParticleIdx)) <= r) {
                neighborList.add(cellParticleIdx);
                result.computeIfAbsent(cellParticleIdx, SET_INSTANTIATOR).add(mainParticleIdx);
            }
        }
    }
}