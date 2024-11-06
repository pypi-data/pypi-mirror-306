<script lang="ts">
	import { type ComponentType } from "svelte";
	export let Icon: ComponentType;
	export let label = "";
	export let show_label = false;
  export let action = "like";
	export let size: "small" | "large" | "medium" = "small";
	export let disabled = false;
	export let hasPopup = false;
	export let color = "var(--block-label-text-color)";
	export let background = "var(--block-background-fill)";
</script>

<button
	{disabled}
	on:click
	aria-label={label}
	aria-haspopup={hasPopup}
	title={label}
	action={action}
	style:--bg-color={!disabled ? background : "auto"}
>
	{#if show_label}<span>{label}</span>{/if}
	<div
		class:small={size === "small"}
		class:large={size === "large"}
		class:medium={size === "medium"}
	>
		<svelte:component this={Icon} />
	</div>
</button>



<style>
	button {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1px;
		z-index: var(--layer-2);
		border-radius: var(--radius-xs);
		color: var(--block-label-text-color);
		border: 1px solid transparent;
		padding: var(--spacing-xxs);
		box-shadow: rgba(0,0,0,0.05) 0px 1px 2px 0px; 
	}

	button:hover {
		cursor: pointer;
		box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1); 
	}

  button:active {
		box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
		background-color: var(--block-label-text-color);
		color: var(--block-background-fill);
	}


	span {
		padding: 0px 1px;
		font-size: 10px;
	}

	div {
		display: flex;
		align-items: center;
		justify-content: center;
		transition: filter 0.2s ease-in-out;
	}

	.small {
		width: 14px;
		height: 14px;
	}

	.medium {
		width: 20px;
		height: 20px;
	}

	.large {
		width: 22px;
		height: 22px;
	}

	@keyframes flash {
		0% {
			opacity: 0.5;
		}
		50% {
			opacity: 1;
		}
		100% {
			opacity: 0.5;
		}
	}




</style>


