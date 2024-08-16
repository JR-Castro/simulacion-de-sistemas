package ar.edu.itba.ss.models;

import java.util.*;
import java.util.function.Function;

public class CIM {
    private final double l;
    private final List<Particle> particles;
    private final double r;
    private final int m;
    private final boolean periodic;

    private static final Function<Integer, Set<Integer>> SET_INSTANTIATOR = x -> new HashSet<>();

    public CIM(Context context) {
        this.l = context.getLength();
        this.particles = context.getParticles();
        this.r = context.getInteractionRadius();
        this.m = context.getMatrixSize();
        this.periodic = context.isPeriodic();
    }

    public int calculateCellIdx(double pos) {
        if (pos * m == l) return m - 1;
        return (int) ((pos * m) / l);
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

        if (!periodic) {
            computeNormalCIM(result, particlesInGrid);
        } else {
            computePeriodicCIM(result, particlesInGrid);
        }

        return result;
    }

    private void computeNormalCIM(Map<Integer, Set<Integer>> result, Cell[][] particlesInGrid) {
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
    }

    private void computePeriodicCIM(Map<Integer, Set<Integer>> result, Cell[][] particlesInGrid) {
        for (int particleIdx = 0; particleIdx < particles.size(); particleIdx++) {
            Particle currentParticle = particles.get(particleIdx);
            int iMatrix = calculateCellIdx(currentParticle.getY());
            int jMatrix = calculateCellIdx(currentParticle.getX());

            Set<Integer> neighborList = result.computeIfAbsent(particleIdx, SET_INSTANTIATOR);

            calculateNeighborsCell(particlesInGrid[iMatrix][jMatrix].getParticles(), particleIdx, neighborList, result);

            if (0 < iMatrix) {
                calculateNeighborsCell(particlesInGrid[iMatrix - 1][jMatrix].getParticles(), particleIdx, neighborList, result);
            } else {
                calculateNeighborsCellPeriodicDownwards(particlesInGrid[m - 1][jMatrix].getParticles(), particleIdx, neighborList, result);
            }

            if (iMatrix < m - 1) {
                calculateNeighborsCell(particlesInGrid[iMatrix + 1][jMatrix].getParticles(), particleIdx, neighborList, result);
            } else {
                calculateNeighborsCellPeriodicVertical(particlesInGrid[0][jMatrix].getParticles(), particleIdx, neighborList, result);
            }

            if (jMatrix < m - 1) {
                calculateNeighborsCell(particlesInGrid[iMatrix][jMatrix + 1].getParticles(), particleIdx, neighborList, result);
            } else {
                calculateNeighborsCellPeriodicHorizontal(particlesInGrid[iMatrix][0].getParticles(), particleIdx, neighborList, result);
            }

            if (iMatrix < m - 1 && jMatrix < m - 1) {
                calculateNeighborsCell(particlesInGrid[iMatrix + 1][jMatrix + 1].getParticles(), particleIdx, neighborList, result);
            } else {
                calculateNeighborsCellPeriodicDiagonal(particlesInGrid[0][0].getParticles(), particleIdx, neighborList, result);
            }
        }
    }

    private void calculateNeighborsCellPeriodicDownwards(TreeSet<Integer> cellParticles, int mainParticleIdx, Set<Integer> neighborList, Map<Integer, Set<Integer>> result) {
        for (int cellParticleIdx : cellParticles) {
            if (mainParticleIdx != cellParticleIdx && calculateDownwardsPeriodicDistance(mainParticleIdx, cellParticleIdx) <= r) {
                neighborList.add(cellParticleIdx);
                result.computeIfAbsent(cellParticleIdx, SET_INSTANTIATOR).add(mainParticleIdx);
            }
        }
    }

    // Important: We are translating the position of the mainParticle as if it was on the next row on the area.
    private double calculateDownwardsPeriodicDistance(int mainParticleIdx, int otherParticleIdx) {
        Particle mainParticle = particles.get(mainParticleIdx);
        Particle otherParticle = particles.get(otherParticleIdx);
        return Math.sqrt(Math.pow(mainParticle.getX() - otherParticle.getX(), 2) + Math.pow(mainParticle.getY() + l - otherParticle.getY(), 2));
    }

    private void calculateNeighborsCellPeriodicDiagonal(TreeSet<Integer> cellParticles, int mainParticleIdx, Set<Integer> neighborList, Map<Integer, Set<Integer>> result) {
        for (int cellParticleIdx : cellParticles) {
            if (mainParticleIdx != cellParticleIdx && calculateDiagonalPeriodicDistance(mainParticleIdx, cellParticleIdx) <= r) {
                neighborList.add(cellParticleIdx);
                result.computeIfAbsent(cellParticleIdx, SET_INSTANTIATOR).add(mainParticleIdx);
            }
        }
    }

    // Important: We are translating the position of the otherParticle as if it was on the next row and column on the area.
    private double calculateDiagonalPeriodicDistance(int mainParticleIdx, int otherParticleIdx) {
        Particle mainParticle = particles.get(mainParticleIdx);
        Particle otherParticle = particles.get(otherParticleIdx);
        return Math.sqrt(Math.pow(mainParticle.getX() - (otherParticle.getX() + l), 2) + Math.pow(mainParticle.getY() - (otherParticle.getY() + l), 2));
    }

    private void calculateNeighborsCellPeriodicVertical(TreeSet<Integer> cellParticles, int mainParticleIdx, Set<Integer> neighborList, Map<Integer, Set<Integer>> result) {
        for (int cellParticleIdx : cellParticles) {
            if (mainParticleIdx != cellParticleIdx && calculateVerticalPeriodicDistance(mainParticleIdx, cellParticleIdx) <= r) {
                neighborList.add(cellParticleIdx);
                result.computeIfAbsent(cellParticleIdx, SET_INSTANTIATOR).add(mainParticleIdx);
            }
        }
    }

    // Important: We are translating the position of the otherParticle as if it was on the next row on the area.
    private double calculateVerticalPeriodicDistance(int mainParticleIdx, int otherParticleIdx) {
        Particle mainParticle = particles.get(mainParticleIdx);
        Particle otherParticle = particles.get(otherParticleIdx);
        return Math.sqrt(Math.pow(mainParticle.getX() - otherParticle.getX(), 2) + Math.pow(mainParticle.getY() - (otherParticle.getY() + l), 2));
    }

    private void calculateNeighborsCellPeriodicHorizontal(TreeSet<Integer> cellParticles, int mainParticleIdx, Set<Integer> neighborList, Map<Integer, Set<Integer>> result) {
        for (int cellParticleIdx : cellParticles) {
            if (mainParticleIdx != cellParticleIdx && calculateHorizontalPeriodicDistance(mainParticleIdx, cellParticleIdx) <= r) {
                neighborList.add(cellParticleIdx);
                result.computeIfAbsent(cellParticleIdx, SET_INSTANTIATOR).add(mainParticleIdx);
            }
        }
    }

    // Important: We are translating the position of the otherParticle as if it was on the next column on the area.
    private double calculateHorizontalPeriodicDistance(int mainParticleIdx, int otherParticleIdx) {
        Particle mainParticle = particles.get(mainParticleIdx);
        Particle otherParticle = particles.get(otherParticleIdx);
        return Math.sqrt(Math.pow(mainParticle.getX() - (otherParticle.getX() + l), 2) + Math.pow(mainParticle.getY() - otherParticle.getY(), 2));
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