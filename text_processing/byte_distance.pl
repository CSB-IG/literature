#!/usr/bin/perl

# use OptArgs;
 
# opt quiet => (
#     isa     => 'Bool',
#     alias   => 'q',
#     comment => 'output nothing while working',
# );
 
# arg item => (
#     isa      => 'Str',
#     required => 1,
#     comment  => 'the item to paint',
# );
 
# my $ref = optargs;
 
# print "Painting $ref->{item}\n" unless $ref->{quiet};


$archivo = 'narco.txt';

%narcos = (
    'El Chapo' => ['El Chapo',
                   'El Chapo Guzmán',
                   'El Chapo Guzman',
                   'El Chapo Guzmán Loera',
                   'El Chapo Guzman Loera',
                   'Joaquín Archivaldo Guzmán Loera',
                   'Joaquín Archivaldo Guzman Loera',
                   'Joaquin Archivaldo Guzmán Loera',
                   'Joaquin Archivaldo Guzman Loera',
                   'Joaquín El Chapo Guzmán',
                   'Joaquin El Chapo Guzman',
                   'Joaquin Guzman Loera',
                   'Joaquín Guzman Loera',
                   'Joaquin Guzmán Loera',
                   'Joaquín Guzmán Loera',
                   'Chapo'],
    'Jolotein' => ['Juan Perez Jolote']
    );


foreach $personaje ( keys %narcos ) {
    foreach $alias (@{$narcos{$personaje}}) {
        $comando = "grep -bo '$alias' $archivo";
        @offsets = `$comando`;
        foreach $linea (@offsets) {
            ($offset, $match) = split(':', $linea);
            print "$personaje\t$offset\n";
        }
    }

}
