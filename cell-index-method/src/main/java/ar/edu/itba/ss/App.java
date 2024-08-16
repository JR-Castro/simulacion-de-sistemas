package ar.edu.itba.ss;

import ar.edu.itba.ss.models.Arguments;
import ar.edu.itba.ss.models.CIM;
import ar.edu.itba.ss.models.Context;
import ar.edu.itba.ss.models.Particle;

import java.io.IOException;
import java.io.Writer;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class App {

    // Args:
    public static void main(String[] cliArgs) throws IOException {
        Arguments args = Arguments.parseArguments(cliArgs);

        Context context = parseInputFiles(args);

        CIM cim = new CIM(context);

        long startTime = System.currentTimeMillis();
        Map<Integer, Set<Integer>> neighbors = cim.compute();
        long endTime = System.currentTimeMillis();

        long duration = endTime - startTime;

        try (Writer output = Files.newBufferedWriter(args.getOutputPath())) {
            output.write(String.format("%d\n", duration));
            for (Map.Entry<Integer, Set<Integer>> entry : neighbors.entrySet()) {
                output.write(String.format("%d ", entry.getKey()));
                for (Integer particle : entry.getValue()) {
                    output.write(String.format("%d ", particle));
                }
                output.write("\n");
            }
        }
    }

    private static Context parseInputFiles(Arguments args) throws IOException {
        List<String> staticFile = Files.readAllLines(args.getStaticPath()).stream().map(s -> s.replaceAll("^ +| +$|( )+", "$1")).toList();
        List<String> dynamicFile = Files.readAllLines(args.getDynamicPath()).stream().map(s -> s.replaceAll("^ +| +$|( )+", "$1")).toList();

        int particleAmount = Integer.parseInt(staticFile.get(0));
        double length = Double.parseDouble(staticFile.get(1));

        List<Particle> particles = new ArrayList<>(particleAmount);
        for (int i = 0; i < particleAmount; i++) {
            String[] staticLine = staticFile.get(i + 2).split(" ");
            String[] dynamicLine = dynamicFile.get(i + 1).split(" ");

            particles.add(new Particle(
                    Double.parseDouble(dynamicLine[0]),
                    Double.parseDouble(dynamicLine[1]),
                    Double.parseDouble(staticLine[0]),
                    Double.parseDouble(staticLine[1])
            ));
        }

        return new Context(length, args.getRc(), args.getM(), particles, args.isPeriodic());
    }
}
