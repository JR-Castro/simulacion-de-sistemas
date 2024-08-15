package ar.edu.itba.ss.models;

import java.nio.file.Files;
import java.nio.file.Path;

public class Arguments {
    private int m = 0;
    private double rc = 0;
    private Path staticPath, dynamicPath;
    private boolean periodic;

    public static Arguments parseArguments(String[] args) {
        Arguments arguments = new Arguments();
        boolean bruteForce = false;
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "-m": // m
                    arguments.m = Integer.parseInt(args[i + 1]);
                    if (arguments.m < 0) {
                        throw new IllegalArgumentException("m must be at least 1");
                    }
                    i++;
                    break;
                case "-rc":
                    arguments.rc = Double.parseDouble(args[i + 1]);
                    i++;
                    break;
                case "-static":
                    arguments.staticPath = Path.of(args[i + 1]);
                    if (!Files.exists(arguments.staticPath) || !Files.isRegularFile(arguments.staticPath)) {
                        throw new IllegalArgumentException("Static input file doesn't exist");
                    }
                    i++;
                    break;
                case "-dynamic":
                    arguments.dynamicPath = Path.of(args[i + 1]);
                    if (!Files.exists(arguments.dynamicPath) || !Files.isRegularFile(arguments.dynamicPath)) {
                        throw new IllegalArgumentException("Dynamic input file doesn't exist");
                    }
                    i++;
                    break;
                case "-periodic":
                    arguments.periodic = true;
                    break;
                case "-brute-force":
                    bruteForce = true;
                    break;
            }
        }

        if (arguments.m == 0 || bruteForce)
            arguments.m = 1;

        if (arguments.dynamicPath == null || arguments.staticPath == null || arguments.rc <= 0 || arguments.m < 0) {
            throw new IllegalArgumentException("Invalid args");
        }

        return arguments;
    }

    public int getM() {
        return m;
    }

    public double getRc() {
        return rc;
    }

    public Path getStaticPath() {
        return staticPath;
    }

    public Path getDynamicPath() {
        return dynamicPath;
    }

    public boolean isPeriodic() {
        return periodic;
    }
}
