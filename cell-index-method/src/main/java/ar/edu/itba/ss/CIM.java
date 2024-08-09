package ar.edu.itba.ss;

public class CIM {
    private final int n;
    private final double l;
    private final double[] ri;
    private final Position[] pi;
    private final int r;
    private final int m;

    public CIM(int n, double l, double[] ri, Position[] pi, int r, int m) {
        this.n = n;
        this.l = l;
        this.ri = ri;
        this.pi = pi;
        this.r = r;
        this.m = m;
    }

    public void compute() {
        Cell[][] particlesInGrid = new Cell[m][m];
        int c;

        for (int i = 0; i < n; i++) {
            c = whereIsParticle(pi[i]);
            particlesInGrid[c / 5][c % 5].addParticle(i);
        }

        for (int i = 0; i < n; i++) {
            c = whereIsParticle(pi[i]);
            int ii = c / 5;
            int iii = c % 5;
            int finalI = i;

            if (ii <= m - 1) {
                particlesInGrid[c / 5 + 1][c % 5].getParticles().forEach((iv) -> {
                    if (pi[finalI].distanceTo(pi[iv]) <= r) {
                        // TODO: Agregar al archivo
                    }
                });
                if (iii <= m - 1) {
                    particlesInGrid[c / 5 + 1][c % 5 + 1].getParticles().forEach((iv) -> {
                        if (pi[finalI].distanceTo(pi[iv]) <= r) {
                            // TODO: Agregar al archivo
                        }
                    });
                }
            }
            if (iii <= m - 1) {
                particlesInGrid[c / 5 + 1][c % 5 + 1].getParticles().forEach((iv) -> {
                    if (pi[finalI].distanceTo(pi[iv]) <= r) {
                        // TODO: Agregar al archivo
                    }
                });
                if (ii > 0) {
                    particlesInGrid[c / 5 - 1][c % 5 + 1].getParticles().forEach((iv) -> {
                        if (pi[finalI].distanceTo(pi[iv]) <= r) {
                            // TODO: Agregar al archivo
                        }
                    });
                }
            }
        }
    }

    private int whereIsParticle(Position p) {
        int i = 0;
        int j = 0;

        i = (int) Math.floor(p.getY() / (l / m));
        j = (int) Math.floor(p.getX() / (l / m));

        return i * 5 + j;
    }
}