package ar.edu.itba.ss;

import ar.edu.itba.ss.models.Arguments;
import ar.edu.itba.ss.models.Context;
import ar.edu.itba.ss.models.Particle;

import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;

public class App {

    // Args:
    public static void main(String[] cliArgs) throws IOException {
        Arguments args = Arguments.parseArguments(cliArgs);

        Context context = parseInputFiles(args);
    }

    private static Context parseInputFiles(Arguments args) throws IOException {
        List<String> staticFile = Files.readAllLines(args.getStaticPath());
        List<String> dynamicFile = Files.readAllLines(args.getDynamicPath());

        int particleAmount = Integer.parseInt(staticFile.get(0));
        double length = Double.parseDouble(staticFile.get(1));

        List<Particle> particles = new ArrayList<>(particleAmount);
        for (int i = 2; i < particleAmount; i++) {
            String[] staticLine = staticFile.get(i).split(" ");
            String[] dynamicLine = dynamicFile.get(i - 1).split(" ");

            particles.add(new Particle(
                    Double.parseDouble(dynamicLine[0]),
                    Double.parseDouble(dynamicLine[1]),
                    Double.parseDouble(staticLine[0]),
                    Double.parseDouble(staticLine[1])
            ));
        }

        return new Context(length, args.getRc(), args.getM(), particles);
    }
}
