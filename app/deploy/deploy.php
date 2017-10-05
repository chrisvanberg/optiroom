<?php
/**
 * Auto Deployment Script for GitHub and Apache.
 *
 *
 * @since deploy 0.1
 */

$auth = md5('SUY^N&vv%np,._@vU"3%L+9M\_D+{SQF'); // set a private hash to validate against, result is your github secret
$target_branch = 'dev'; // this is the absolute branch to track
$log_path = './deployment.log'; // path can be relative to this script or absolute
$raw_post = NULL;

if ( !empty($_POST['payload']) ) {
	$payload = $_POST['payload'];
	if ( ! is_array($payload) || empty($payload) ) {
		$payload = json_decode(stripslashes($_POST['payload']), true);
	}
	$hmac = $_SERVER['HTTP_X_HUB_SIGNATURE'];
	$payload['hmac']['details'] = array(
		'hmac' => $hmac,
		'auth' => $auth
	);
	if ( empty($hmac) ) {
		$payload['hmac'][] = ("HTTP header 'X-Hub-Signature' is missing.");
	} elseif (!extension_loaded('hash')) {
		$payload['hmac'][] = ("Missing 'hash' extension to check the secret code validity.");
	}
	list($algo, $hash) = explode('=', $hmac, 2) + array('', '');
	$payload['hmac']['details']['algo'] = $algo;
	$payload['hmac']['details']['hash'] = $hash;
	if (!in_array($algo, hash_algos(), TRUE)) {
		$payload['hmac'][] = ("Hash algorithm '$algo' is not supported.");
	}
	$raw_post = file_get_contents('php://input');
	if ($hash !== hash_hmac($algo, $raw_post, $auth)) {
		$payload['hmac'][] = ('Hook secret does not match.');
	}
	$payload['whoami'] = exec('whoami');
	$post_data = sprintf("<pre>%s</pre>", print_r($payload, true));
	
	shell_exec("cat > $log_path <<DELIM\n$post_data\nDELIM");
} else {
	$post_data = sprintf("<pre>%s</pre>", print_r(array($_GET, $_POST, $_REQUEST), true));
	shell_exec("cat > $log_path <<DELIM\n$post_data\nDELIM");
	exit;
}

if ( is_array($payload) && !empty($payload['ref']) ) {
	$branch = array_pop( explode('/', $payload['ref']) );
}
$commit = !empty($payload['after']) ? $payload['after'] : "HEAD";
if (empty($branch) || $target_branch !== $branch ) {
	shell_exec("cat >> $log_path <<DELIM\nInvalid Branch: $branch\nDELIM");
}

/**
 * @internal array properties must be curated per the target system
 */
$args = array(
	'target' => './',
	'git' => '/usr/local/bin/git',
	'mailto' => 'contact@chrosv.be',
	'commands' => array(
		'echo $PWD',
		"git branch",
		"git fetch --all",
		"git stash save --keep-index",
		"git reset --hard $commit",
		"git pull origin $target_branch",
		"git status",
		"git rev-parse HEAD | cut -c1-7",
	)
);

/**
 * Function handles the output and executes the deployment commands
 * @param $args array - see @internal notes above
 * @return string html output
 */
function deploy($args) {
	chdir( $args['target'] );
	$git = trim(exec('which git'));
	if (empty($git)) $git = $args['git'];
	$whoami = trim(shell_exec('whoami'));
	$output = array(
		"<b>$whoami\$ php deploy.php</b>",
		"<span>Git Deployment Script, version 0.1 (apache)",
		"Creative Commons Attribution-NoDerivs 3.0 Unported",
		"Copyright (C) 2013 Wes Turner, Barrel LLC, All Rights Reserved</span>"
	);
	foreach($args['commands'] as $command){
		$command = str_replace('git', $git, $command);
		$tmp = shell_exec($command);
		if (empty($tmp)) $tmp = "No output.";
		$output[] = "<b>$whoami\$ {$command}\n</b>".htmlentities(trim($tmp));
	}
	$return = implode("\n", $output);
	if ( $args['mailto'] ) {
		$headers  = 'MIME-Version: 1.0' . "\r\n";
		$headers .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n";
		$headers .= 'From: '.$args['mailto'] . "\r\n" .
		$headers .= 'Reply-To: '.$args['mailto'] . "\r\n" .
		$headers .= 'X-Mailer: PHP/' . phpversion();
		mail( $args['mailto'], 'Latest commit deployed', $output, $headers );
	}
	return $return;
} 
ob_start();
?>
<!DOCTYPE HTML>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<title>deploy.php</title>
<style>
body {
	background-color: black;
	line-height: 1.1em;
	margin: 0;
}
pre {
	background-color: black;
	color: white;
	margin: 0;
	padding: 5%;
	white-space: pre-line;
}
span {
	color: #829AAE;
}
b {
	color: #6BE234;
	font-weight: normal;
}
</style>
</head>
<body>
<pre>
<?php echo deploy($args); ?>
</pre>
</body>
</html>
<?php 
$output = ob_get_clean();
// note this log file will be relative to the last path changed
shell_exec("cat > ./deployment.html <<DELIM\n$output\nDELIM"); 
?>
